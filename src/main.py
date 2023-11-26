from dotenv import load_dotenv

load_dotenv()

from rich.console import Console

from tasks import headings, writing
from models import group_headings


# * Project start
console = Console()

title = "Toothpaste"

sections = headings.generate_headings(title)
grouped = group_headings(sections)

section = writing.write_section(
    section=grouped[0], heading=grouped[0].headings[0], title=title
)

# print(section)

# console.print(Markdown(section))
