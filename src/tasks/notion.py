import os
import re
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])


def split_url(url: str):
    matches = re.search(r"\/(\w+)\?v=", url)
    if not matches:
        # ? Should raise exception here?
        return None

    return matches.group(1)


def create_primary_page(database: str, title: str, category: str):
    payload = {
        # "cover": {
        #     "type": "external",
        #     "external": {
        #         "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
        #     },
        # },
        "icon": {
            "type": "emoji",
            "emoji": "🥬",
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
    return notion.pages.create(**payload)


def create_subpage():
    ...
