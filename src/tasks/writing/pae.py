from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from config.models import EnabledModels

from models import Heading, Section


def plan_and_execute(section: Section, heading: Heading, title: str):
    search = DuckDuckGoSearchAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. Ask targeted questions.",
        ),
    ]

    model = ChatOpenAI(temperature=0, model=EnabledModels.WRITING)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor)

    message = """
    You are an expert researcher. You should attempt to write high quality, lengthy and informative research on a given topic. Your research should be heavily formatted using markdown.
    Write an informational knowledge piece on the topic {objective}. You are writing for a larger knowledgebase with the title: '{title}'.
    Your section context is:
    `
{section}
`
    Only write about section {objective}, you can refer to other sections, but they are only for context, all information you write should align with the {objective}
    """.format(
        title=title,
        section=section.format(),
        objective=f"'{heading.index}: {heading.title}'",
    )

    return agent.run(message)
