from dotenv import load_dotenv

load_dotenv()

from rich.console import Console

from pathlib import Path

from tasks import headings, writing


def write(section, title):
    p = Path("./generated/")
    p.mkdir(parents=True, exist_ok=True)
    fn = f"{title}.md"
    filepath = p / fn
    with filepath.open("w", encoding="utf-8") as f:
        f.write(section.dump())


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

    write(section, title)
    break
