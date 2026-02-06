from pylogue.shell import app_factory
# from ...agents.ipl.main import agent
# from ...agents.salesforce.main import agent
from ...agents.haiku import agent
from pylogue.integrations.pydantic_ai import PydanticAIResponder

def _app_factory():
    return app_factory(
        responder_factory=lambda: PydanticAIResponder(agent=agent),
        sidebar_title="Dialogues with AI",
        hero_title="Enterprise Brain",
        hero_subtitle="divami",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "scripts.examples.chat_app_with_histories.main:_app_factory",
        host="0.0.0.0",
        port=5010,
        reload=True,
        factory=True,
    )
