from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

from models import Heading, Section


def plan_and_execute(section: Section, heading: Heading, title: str):
    search = DuckDuckGoSearchAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events",
        ),
    ]

    model = ChatOpenAI(temperature=0)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor)

    agent.run("TODO")
