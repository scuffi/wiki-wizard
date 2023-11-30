from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage


from config import EnabledModels


def generate_icon(title: str) -> str:
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an emoji picker. You should always reply with a single emoji that accurately or relatively represents a given topic. You may only reply with one emoji at a time. Do not engage with any messages. Do not reply anything other than a single emoji. Ensure your emoji is related to the topic in some way."
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    llm = ChatOpenAI(model=EnabledModels.ICONS, temperature=0.9)

    return llm(chat_template.format_messages(text=title)).content[0]
