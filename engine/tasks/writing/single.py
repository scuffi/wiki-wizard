from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor

from models import Heading, ModelConfig


def single_prompt(
    section: str, heading: Heading, title: str, model_config: ModelConfig
):
    search = DuckDuckGoSearchAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for searching for accurate information. Ask targeted questions.",
        ),
    ]

    llm = ChatOpenAI(
        model=model_config.writing, temperature=0, api_key=model_config.oai_key
    )
    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert researcher. You should attempt to write high quality, lengthy and informative research on a given topic. Your research should be heavily formatted using markdown. Your research should be a long, text based informational page, ensure you write in depth and maintain the quality of knowledge. Do not include the given title you are writing about or the index of the title."
                    "Write in British English."
                ),
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
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
        section=section,
        objective=f"'{heading.index}: {heading.title}'",
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools)

    return agent_executor.invoke({"input": message})["output"]
