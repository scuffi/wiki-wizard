from models import Heading, Section, ModelConfig

from .agents import double_agent
from .pae import plan_and_execute
from .single import single_prompt


class WritingMethod:
    DOUBLE_AGENT = double_agent
    SINGLE = single_prompt
    PAE = plan_and_execute


# @monitor("[bold green]Writing section...")
def write_section(
    section: Section,
    heading: Heading,
    title: str,
    model_config: ModelConfig,
    method: WritingMethod = WritingMethod.DOUBLE_AGENT,
    *args,
    **kwargs,
):
    """
    The `write_section` function takes in various parameters and uses a specified writing method to
    write a section with a heading and title using a model configuration.

    Args:
      section (Section): The `section` parameter is an instance of the `Section` class, which represents
    a section of a document or text.
      heading (Heading): The `heading` parameter is of type `Heading` and represents the heading of the
    section. It is used to provide a title or description for the section.
      title (str): A string representing the title of the section.
      model_config (ModelConfig): The `model_config` parameter is an instance of the `ModelConfig`
    class. It contains configuration settings for a model.
      method (WritingMethod): The `method` parameter is an optional parameter of type `WritingMethod`
    that specifies the writing method to be used. It has a default value of
    `WritingMethod.DOUBLE_AGENT`.

    Returns:
      the result of calling the `method` function with the provided arguments.
    """
    return method(
        section=section,
        heading=heading,
        title=title,
        model_config=model_config,
        *args,
        **kwargs,
    )


def write_section_mp(args: tuple[str, Heading, str, WritingMethod, ModelConfig]):
    """
    The function `write_section_mp` takes in a tuple of arguments and uses them to call a specified
    writing method with the given section, heading, title, and model configuration.

    Args:
      args (tuple[str, Heading, str, WritingMethod, ModelConfig]): A tuple containing the following
    elements: `section, heading, title, method, model_config`

    Returns:
      The function `write_section_mp` returns the result of calling the `method` function with the
    provided arguments.
    """
    section, heading, title, method, model_config = args
    return method(
        section=section,
        heading=heading,
        title=title,
        model_config=model_config,
    )
