from dotenv import load_dotenv

load_dotenv()


from rich import print

from tasks import notion, headings, writing, icons


# * Project start
title = "Toothpaste"

database_id = notion.split_url(
    "https://www.notion.so/archief/93992d8440fa4111b06e7cc5748fac5e?v=6429bb958ce6452497c5089c15e9e6f2"
)

primary_page = notion.create_primary_page(
    database_id, title=title, category="Programming", icon=icons.generate_icon(title)
)

notion.write_to_page(
    primary_page,
    [{"type": "table_of_contents", "table_of_contents": {"color": "default"}}],
)

sections = headings.generate_headings(title)

for section in sections:
    for node in section.tree:
        heading = node.data

        page = primary_page

        content = notion.parse_to_notion(
            f"#{'#'*heading.index.count('.')} {heading.index} - {heading.title}"
        )

        print(content)

        notion.write_to_page(page, content)

        if node.is_leaf():
            written_section = writing.write_section(
                section=section, heading=heading, title=title
            )
            heading.content = written_section
            parsed = notion.parse_to_notion(written_section)

            notion.create_subpage(
                page,
                title=heading.title,
                icon=icons.generate_icon(heading.title),
                content=parsed,
            )

    break
