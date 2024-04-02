from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage

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

    llm = ChatOpenAI(temperature=0, model=EnabledModels.WRITING)

    planner = load_chat_planner(llm)
    executor = load_agent_executor(llm, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor)

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an expert researcher. You should attempt to write high quality, lengthy and informative research on a given topic. Your research should be heavily formatted using markdown. Your research should be a long, text based informational page, ensure you write in depth and maintain the quality of knowledge."
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    message = """
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

    return agent.run(chat_template.format_messages(text=message))
