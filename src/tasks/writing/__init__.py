from console import monitor
from models import Heading, Section

from .writer import double_agent, single_prompt, plan_and_execute


class WritingMethod:
    DOUBLE_AGENT = double_agent
    SINGLE = single_prompt
    PAE = plan_and_execute


@monitor("[bold green]Writing section...")
def write_section(
    section: Section,
    heading: Heading,
    title: str,
    method: WritingMethod = WritingMethod.DOUBLE_AGENT,
    *args,
    **kwargs,
):
    return method(section=section, heading=heading, title=title, *args, **kwargs)
