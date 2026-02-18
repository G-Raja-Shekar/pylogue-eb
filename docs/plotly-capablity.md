# 📊 Salesforce Data Visualization with Plotly

## Overview

The Salesforce Agent enables natural language querying of Salesforce data with automatic interactive visualizations powered by Plotly. The agent intelligently selects the optimal graph type based on your data structure and query intent.

## 🎯 Quick Reference

| Data Type | Best For | Graph Type |
|-----------|----------|------------|
| Category + Value | Comparing categories | Bar Chart |
| Date + Value | Trends over time | Line Chart |
| Category distribution | Percentage breakdown | Pie Chart |
| Pipeline stages | Sales funnel | Funnel Chart |
| Numeric vs Numeric | Correlations | Scatter Plot |
| Numeric distribution | Frequency analysis | Histogram |
| Category + Numeric spread | Statistical analysis | Box Plot |
| Two categories | 2D comparison | Heatmap |
| Hierarchy | Nested data | Treemap |
| Location data | Geographic insights | Map |
| Raw records | Detailed view | Table |

## 📈 Supported Visualizations

### 📊 Bar Chart - Category Comparison
**Use for:** Comparing values across different categories

**Example queries:**
- "Show Opportunity count by Stage"
- "Show total Opportunity Amount by Stage"
- "Show Cases by Priority"
- "Show Accounts by Industry"

### 📉 Line Chart - Trends Over Time
**Use for:** Analyzing temporal patterns

**Example queries:**
- "Show Opportunity trend over time"
- "Show revenue trend by month"
- "Show Cases created per day"

### 🥧 Pie Chart - Distribution
**Use for:** Visualizing proportional breakdowns

**Example queries:**
- "Show Opportunity distribution by Stage"
- "Show Cases distribution by Status"
- "Show Leads distribution by Source"

### 🔻 Funnel Chart - Sales Pipeline
**Use for:** Tracking conversion through stages

**Example queries:**
- "Show Opportunity funnel by Stage"
- "Show sales pipeline funnel"
- "Show Lead conversion funnel"

### 🔵 Scatter Plot - Numeric Relationships
**Use for:** Analyzing correlations between two numeric fields

**Example queries:**
- "Show Opportunity Amount vs Probability"
- "Show Expected Revenue vs Amount"

### 📊 Histogram - Numeric Distribution
**Use for:** Understanding frequency distributions

**Example queries:**
- "Show distribution of Opportunity Amount"
- "Show distribution of deal sizes"

### 📦 Box Plot - Statistical Spread
**Use for:** Displaying median, quartiles, and outliers

**Example queries:**
- "Show Opportunity Amount distribution by Stage"
- "Show revenue distribution by Industry"

### 🔥 Heatmap - 2D Category Comparison
**Use for:** Comparing two categorical dimensions

**Example queries:**
- "Show Opportunities by Stage and Owner"
- "Show Cases by Status and Priority"

### 📈 Area Chart - Cumulative Trends
**Use for:** Visualizing growth and accumulation

**Example queries:**
- "Show cumulative Opportunity Amount over time"
- "Show revenue growth over time"

### 🗂️ Treemap - Hierarchical Data
**Use for:** Nested categorical relationships

**Example queries:**
- "Show Opportunity Amount by Stage and Owner"
- "Show revenue by Industry and Account"

### 🗺️ Geographic Map - Location Data
**Use for:** Spatial data visualization

**Example queries:**
- "Show Accounts by Country on map"
- "Show revenue by Region"
- "Show Customers by State"

### 📋 Table View - Structured Data
**Use for:** Detailed record inspection

**Example queries:**
- "Show top 10 Opportunities by Amount"
- "Show all open Cases"
- "Show latest Leads"

## 💡 Benefits

- **Natural Language Interface** - No need to build manual reports
- **Automatic Chart Selection** - Plotly intelligently chooses the best visualization
- **Interactive Exploration** - Zoom, filter, and drill down in real-time
- **Real-time Data** - Always current Salesforce data
- **Improved Decision-Making** - Visual insights for faster analysis
