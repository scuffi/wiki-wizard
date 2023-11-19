from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage


gpt35 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a planning agent. Your only goal is to breakdown a given prompt into different sections. Each section should be an interesting aspect of the topic. Each section should have an extensive array of sub-sections to cover all possible areas of the topic. You should treat each message as a topic you need to break down. Do not engage with the message itself."
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

llm = ChatOpenAI(model=gpt35, temperature=0.6)
llm(chat_template.format_messages(text="Toothpaste"))