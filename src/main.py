from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
from rich.markdown import Markdown

from tasks import headings, writing


# * Project start
console = Console()

title = "Toothpaste"

sections = headings.generate_headings(title)

for section in sections:
    for heading in section.get_writable_headings():
        written_section = writing.write_section(
            section=section, heading=heading, title=title
        )
        heading.content = written_section
        break
    break

print(heading)

console.print(Markdown(written_section))
