import autogen

from console import monitor
from models import Heading, Section
from config import AutoGen, GPT35, GPT4, EnabledModels

llm_config = (
    {"config_list": AutoGen.CONFIG_LIST_GPT3, "seed": 42, "model": GPT35}
    if EnabledModels.WRITING == GPT35
    else {"config_list": AutoGen.CONFIG_LIST_GPT4, "seed": 42, "model": GPT4}
)


@monitor("[bold green]Writing section...")
def write_section(section: Section, heading: Heading, title: str):
    # TODO: Fix all the system messages here, incorporate scoring system to ensure outputs don't get worse, make use of all 128k context size.
    researcher = autogen.AssistantAgent(
        name="Researcher",
        system_message="Research Assistant. Your only goal is to provide high quality, detailed information on the topic given to you structured in markdown. If you are given improvements, you must use those comments to improve your previous response, do not write a new answer, it must be the previous answer incorporating the changes. You must ensure that you understand the topic and create a detailed and informative set of research on the topic. You should always reply with long, detailed research. Your research should always be structured using markdown. If you are prompted with improvements, use those improvements to improve your last set of research. Do not include the title you are writing for anywhere in your response. Do not engage in any conversation in anyt circumstance.",
        llm_config=llm_config,
    )
    qa = autogen.AssistantAgent(
        name="Quality_Assurer",
        system_message="Quality Assurer. You are a quality assurer and should critique, comment and suggest tweaks to a given set of information and return the comments to the Researcher. You should always try to find improvements in a message. You will recieve information from a research agent, and it is your job to ensure that research is up to a high standard. You should help the researcher make more enformed writing choices in your comments. You should advise the researcher on different topics to go into depth into, add examples, and anything else that could improve the quality, accuracy and depth of a given block of information. You should not write or edit the information yourself, only provide high quality and accurate comments. If the message meets the given requirements, do not add any comments or anything else to your response, only reply with ONLY the word: 'TERMINATE' in all capital letters. Do not engage in any conversation in anyt circumstance. If you have no comments, reply with 'TERMINATE' in all capitals.",
        llm_config=llm_config,
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

    qa.initiate_chat(
        researcher,
        message=message,
    )

    return qa.chat_messages[researcher][1]["content"]
