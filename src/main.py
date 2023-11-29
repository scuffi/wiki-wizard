from dotenv import load_dotenv

load_dotenv()


from pathlib import Path

from tasks import notion, headings, writing, parsing


def write(section, title):
    p = Path("./generated/")
    p.mkdir(parents=True, exist_ok=True)
    fn = f"{title}.md"
    filepath = p / fn
    with filepath.open("w", encoding="utf-8") as f:
        f.write(section.dump())


# * Project start
database_id = notion.split_url(
    "https://www.notion.so/archief/93992d8440fa4111b06e7cc5748fac5e?v=6429bb958ce6452497c5089c15e9e6f2"
)
# notion.create_primary_page(database_id, title="Python", category="Programming")
# console = Console()

title = "Toothpaste"

sections = headings.generate_headings(title)

for section in sections:
    for heading in section.get_writable_headings():
        written_section = writing.write_section(
            section=section, heading=heading, title=title
        )
        heading.content = written_section
        parsed = parsing.parse2notion(written_section)
        print(parsed.valueOf())
        print(type(parsed.valueOf()))
        break

    # write(section, title)
    break
