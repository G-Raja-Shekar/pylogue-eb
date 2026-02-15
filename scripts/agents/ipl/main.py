import duckdb
import json
import pandas as pd
from pathlib import Path
from pydantic_ai import Agent
from pylogue.core import main as create_core_app
from pylogue.dashboarding import render_plotly_chart_py
import logfire
from pylogue.integrations.pydantic_ai import PydanticAIResponder

logfire.configure()
logfire.instrument_pydantic_ai()

instructions = """
You analyze IPL match data stored in CSV files. 
You can read CSV files, summarize data, and answer questions about IPL matches.
When we went to purchase. Watch They made us pay only through Apple Pay. Apple Watch. Only Apple pays a lot. Of last game. But he said Apple figure he started with Apple. Amazon is also like that. No pays Amazon pay, then we'll give you discount. The two tables given are 'matches' and 'deliveries', containing match-level and ball-level data respectively.
Always Use read_csv_with_schema to inspect the structure and sample data of these tables instead of guessing.
Use execute_sql_on_csv to run SQL queries on these tables to extract insights.
Before any complex SQL, call read_csv_with_schema on the relevant tables.
Only use columns that exist in the schema. Never invent aliases or columns.
Start with a LIMIT 5 validation query to confirm column names and joins.
If a column or table is missing, ask for clarification instead of guessing.
Never reference an alias unless it is defined in the FROM clause.
For year-based filters, first query the latest year from the correct table and use it as the default.
If the user's question is vague, ask for clarification.
You can also build interactive Plotly dashboards by calling render_plotly_chart with a SELECT query and Plotly-Python code that defines a `fig` variable. Keep queries small (<2000 rows).
When using render_plotly_chart, you may use import statements if needed.
In chart code, use the provided `df` variable directly (a `data` alias may exist for compatibility).
For linked two-chart interactions, always encode the click contract in
`fig.update_layout(meta={"pylogue_linked_interaction": ...})`:
- `source_trace`: trace index to click (typically left chart).
- `target_trace`: trace index to update (typically right chart).
- `season_menu_index`: dropdown index for active season (usually 0).
- `default_season`: initial season label.
- `target_title_annotation_index`: subplot title annotation index to update (for 2 subplots this is usually 1).
- `lookup`: map each key `"<season>||<team>"` to payload dict with `x`, `y`, `text`, optional `customdata`, and `title`.
Build `lookup` for every season/team combination from `df` so bar clicks can always update the right chart.
Available tables are registered from local CSVs (e.g., matches, deliveries); query them directly.
Every tool call must include a `purpose` argument that briefly and non-technically states what the tool is about to do.
Use read_vega_doc to fetch Vega/Vega-Lite specs from URLs before deciding to render charts.

You will talk in less than 200 words at a time. You will not generate tables, diagrams or reasons unless asked.
Note that the end user is not familiar with SQL or data analysis, so don't bother giving technical details what so ever.
Before generating a plot, you will first confirm the behavior and design with the user in non-technical terms, and only after their confirmation, you will generate the plot.

ALWAYS FIRST READ THE SCHEMA
"""

agent = Agent(
    # "openai:gpt-5-mini",
    "google-gla:gemini-3-flash-preview",
    instructions=instructions,
)
deps = None

DATA_DIR = Path(__file__).resolve().parent


def _normalize_sql_query(sql_query: str) -> str:
    query = (sql_query or "").strip()
    if query.startswith("```"):
        query = query.strip("`")
        if query.lower().startswith("sql\n"):
            query = query[4:]
    if (query.startswith('"') and query.endswith('"')) or (
        query.startswith("'") and query.endswith("'")
    ):
        query = query[1:-1]
    query = (
        query.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace("\\r", "\r")
        .strip()
        .rstrip(";")
    )
    return query


def register_csv_views(conn: duckdb.DuckDBPyConnection, csv_path: str | None = None):
    """Register CSV files as DuckDB views for convenient querying.

    - If csv_path is provided, only that file is registered.
    - Otherwise, all top-level CSV files alongside this script are registered.
    """

    targets = [Path(csv_path)] if csv_path else list(DATA_DIR.glob("*.csv"))

    for csv_file in targets:
        alias = csv_file.stem.replace("-", "_")
        conn.execute(
            f"CREATE OR REPLACE VIEW {alias} AS SELECT * FROM read_csv_auto('{csv_file.as_posix()}')"
        )


# Eagerly register known CSVs on startup so tools can query by table name (e.g., matches, deliveries)
_startup_conn = duckdb.connect()
register_csv_views(_startup_conn)
_startup_conn.close()

@agent.tool_plain()
def read_csv_with_schema(table: str, purpose: str):
    """Show schema + sample for a registered CSV table (avoids sending full data)."""
    conn = duckdb.connect()
    register_csv_views(conn)  # ensure views exist

    # Sample the first 50 rows instead of loading the whole file
    sample_df = conn.execute(
        f"SELECT * FROM {table} LIMIT 50"
    ).df()

    # Get schema info
    schema_df = conn.execute(
        f"DESCRIBE SELECT * FROM {table}"
    ).df()

    # Count rows without materializing the table
    row_count = conn.execute(
        f"SELECT COUNT(*) AS rows FROM {table}"
    ).fetchone()[0]

    print("Schema:")
    print(schema_df)
    print(f"\nTotal Rows: {row_count}")
    print("\nSample rows:")
    print(sample_df.head())

    return {
        "sample_csv": sample_df.to_csv(index=False),
        "schema_csv": schema_df.to_csv(index=False),
        "row_count": row_count,
    }

@agent.tool_plain()
def execute_sql_on_csv(sql_query: str, purpose: str) -> str:
    """Execute a SELECT against registered CSV tables. Avoid 1000s of rows."""
    conn = duckdb.connect()
    register_csv_views(conn)

    # allow only select queries
    sql_query = _normalize_sql_query(sql_query)
    # black_list_cmds = ["insert", "update", "delete", "create", "drop", "alter"]
    # if any(
    #     cmd in sql_query for cmd in black_list_cmds
    # ):
    #     return "Error: Only SELECT queries are allowed."
    result_df = conn.execute(sql_query).df()

    print(f"Executed SQL: {sql_query}")
    print(f"Result rows: {len(result_df)}")
    print(result_df.head())

    return result_df.to_csv()


@agent.tool_plain()
def render_plotly_chart(sql_query: str, plotly_python: str, purpose: str):
    """Render a Plotly chart using Python code that defines `fig`."""
    conn = duckdb.connect()
    register_csv_views(conn)

    # Enforce SELECT-only
    normalized_query = _normalize_sql_query(sql_query)
    if not normalized_query.lower().startswith("select"):
        return "Error: Only SELECT queries are allowed. Reference registered tables like matches or deliveries."

    def _sql_query_runner(query: str):
        normalized_inner = _normalize_sql_query(query)
        limited_query = f"SELECT * FROM ({normalized_inner}) t LIMIT 2000"
        return conn.execute(limited_query).df().to_dict(orient="records")

    return render_plotly_chart_py(
        sql_query_runner=_sql_query_runner,
        sql_query=normalized_query,
        plotly_python=plotly_python,
    )
