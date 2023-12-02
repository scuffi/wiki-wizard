from dotenv import load_dotenv

load_dotenv()


from rich import print

from tasks import notion, headings, writing, icons, WritingMethod

# TODO: Migrate Agents into GPTs in OpenAI, allowing central control & configuration of each agent.
# TODO: See - https://www.youtube.com/watch?v=AVInhYBUnKs&t=479s

# * Project start
title = "Anne Boleyn"

database_id = notion.split_url(
    "https://www.notion.so/archief/93992d8440fa4111b06e7cc5748fac5e?v=6429bb958ce6452497c5089c15e9e6f2"
)

primary_page = notion.create_primary_page(
    database_id, title=title, category="General", icon=icons.generate_icon(title)
)

try:
    notion.write_to_page(
        primary_page,
        [
            {"type": "table_of_contents", "table_of_contents": {"color": "default"}},
            {"type": "divider", "divider": {}},
        ],
    )

    sections = headings.generate_headings(title)

    print([section.dump() for section in sections])

    for section in sections:
        for node in section.tree:
            heading = node.data

            if node.is_leaf():
                written_section = writing.write_section(
                    section=section,
                    heading=heading,
                    title=title,
                    method=WritingMethod.PAE,
                )
                heading.content = written_section
                parsed = notion.parse_to_notion(written_section)

                notion.create_subpage(
                    primary_page,
                    title=heading.title,
                    icon=icons.generate_icon(heading.title),
                    content=parsed,
                )
            else:
                # * Only write title in case we don't create page > should this be configurable
                content = notion.parse_to_notion(
                    # f"#{'#'*heading.index.count('.')} {heading.index} - {heading.title}" # ? MAke this configurable option
                    f"#{'#'*heading.index.count('.')} {heading.title}"
                )

                print(content)

                notion.write_to_page(primary_page, content)

        break
    notion.update_status(primary_page, "Done")
except Exception as ex:
    notion.update_status(primary_page, "Failed")
    print(ex)
