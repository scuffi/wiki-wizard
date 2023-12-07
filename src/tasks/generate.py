from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage


from models import Model


def prompt(prompt: str, system_message: str, model: Model, **kwargs) -> str:
    """
    The `prompt` function takes in a prompt, a system message, a model configuration, and an optional
    temperature value. It creates a chat template using the prompt and system message, and then uses the
    OpenAI API to generate a response based on the template and model configuration. The generated
    response is returned as a string.

    Args:
      prompt (str): The `prompt` parameter is a string that represents the initial message or question
    that you want to ask the model.
      system_message (str): The `system_message` parameter is a string that represents a message from
    the system or the assistant. It is typically used to provide context or instructions to the user
    before they provide their input.
      model_config (ModelConfig): The `model_config` parameter is an object that contains the
    configuration for the language model. It typically includes the following properties:
      temperature (float): The `temperature` parameter is a value that controls the randomness of the
    generated text. A higher temperature value (e.g., 1.0) will result in more random and diverse
    responses, while a lower temperature value (e.g., 0.2) will produce more focused and deterministic
    responses. Defaults to 0

    Returns:
      The `prompt` function returns a string.
    """
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    llm = ChatOpenAI(
        model=model.model,
        temperature=model.temperature,
        api_key=model.key,
    )

    return llm(chat_template.format_messages(text=prompt, **kwargs)).content
