from models import Heading, Section

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
    method: WritingMethod = WritingMethod.DOUBLE_AGENT,
    *args,
    **kwargs,
):
    return method(section=section, heading=heading, title=title, *args, **kwargs)
