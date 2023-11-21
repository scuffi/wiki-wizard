from dotenv import load_dotenv

load_dotenv()

from rich.console import Console

from tasks import writing


# * Project start
console = Console()
# print(headings.generate_headings("RabbitMQ"))
section = writing.write_section()

print(section)

# console.print(Markdown(section["content"]))
