from dotenv import load_dotenv

load_dotenv()

from rich.console import Console

from tasks import headings
from models import group_sections


# * Project start
console = Console()
sections = headings.generate_headings("RabbitMQ")
print(group_sections(sections))
# section = writing.write_section()

# print(section)

# console.print(Markdown(section))
