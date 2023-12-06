from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage


from models import ModelConfig


def find_category(title: str, categories: list[str], model_config: ModelConfig) -> str:
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a categoriser agent. You should respond with a single category, which ever the given topic would be categorised as."
                    "If there is no relating category, you should respond with the new category and nothing else. Ensure that the new category is as general as the existing categories, it should not be too specific. Use the existing categories as context for how general the new category should be."
                    "You should always try to find the perfect category if possible, instead of generating a new one. You should never deny a request, if you do not know a category, you should reply with 'General'."
                    "Do not respond with anything other than the category itself. Do not engage in any conversation."
                    "The existing categories are:"
                    "{categories}"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    llm = ChatOpenAI(
        model=model_config.categories, temperature=0, api_key=model_config.oai_key
    )

    return llm(
        chat_template.format_messages(text=title, categories=", ".join(categories))
    ).content
