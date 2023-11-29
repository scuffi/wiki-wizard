import os
import re
from notion_client import Client
from javascript import require

# * Martian is an external JS package built to convert markdown/text into notion blocks
# https://github.com/tryfabric/martian
# * We have to use an awesome javascript bridge to use this package as there is no python bindings
martian = require("@tryfabric/martian")

notion = Client(auth=os.environ["NOTION_TOKEN"])


def parse_to_notion(markdown: str):
    """Parse a markdown text string into valid Notion Blocks/JSON API text

    Args:
        markdown (str): The markdown string

    Returns:
        list[any]: The parsed MD text in JSON format
    """
    return martian.markdownToBlocks(markdown).valueOf()


def split_url(url: str):
    matches = re.search(r"\/(\w+)\?v=", url)
    return matches[1] if matches else None


def write_to_page(page_id: str, blocks: list):
    notion.blocks.children.append(page_id, children=blocks)


def create_primary_page(database: str, title: str, category: str, icon: str):
    payload = {
        # "cover": {
        #     "type": "external",
        #     "external": {
        #         "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
        #     },
        # },
        "icon": {
            "type": "emoji",
            "emoji": icon,
        },
        "parent": {
            "type": "database_id",
            "database_id": database,
        },
        "properties": {
            # "title": {"title": [{"text": {"content": "Tuscan kale"}}]},
            "Name": {"title": [{"text": {"content": title}}]},
            # "Description": {
            #     "rich_text": [{"text": {"content": "A dark green leafy vegetable"}}]
            # },
            "Category": {
                "select": {
                    "name": category,
                },
            },
        },
        # "children": [
        #     {
        #         "object": "block",
        #         "heading_2": {"rich_text": [{"text": {"content": "Lacinato kale"}}]},
        #     },
        #     {
        #         "object": "block",
        #         "paragraph": {
        #             "rich_text": [
        #                 {
        #                     "text": {
        #                         "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
        #                         "link": {
        #                             "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
        #                         },
        #                     },
        #                     "href": "https://en.wikipedia.org/wiki/Lacinato_kale",
        #                 }
        #             ],
        #             "color": "default",
        #         },
        #     },
        # ],
    }
    return notion.pages.create(**payload)["id"]


def create_subpage(primary_page: str, title: str, icon: str, content: list | None):
    payload = {
        # "cover": {
        #     "type": "external",
        #     "external": {
        #         "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
        #     },
        # },
        "icon": {
            "type": "emoji",
            "emoji": icon,
        },
        "parent": {
            "type": "page_id",
            "page_id": primary_page,
        },
        "properties": {
            "title": {"title": [{"text": {"content": title}}]},
        },
        # "children": [
        #     {
        #         "object": "block",
        #         "heading_2": {"rich_text": [{"text": {"content": "Lacinato kale"}}]},
        #     },
        #     {
        #         "object": "block",
        #         "paragraph": {
        #             "rich_text": [
        #                 {
        #                     "text": {
        #                         "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
        #                         "link": {
        #                             "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
        #                         },
        #                     },
        #                     "href": "https://en.wikipedia.org/wiki/Lacinato_kale",
        #                 }
        #             ],
        #             "color": "default",
        #         },
        #     },
        # ],
    }

    if content:
        payload["children"] = content

    return notion.pages.create(**payload)["id"]
