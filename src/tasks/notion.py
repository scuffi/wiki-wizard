import os
import re
import random
from notion_client import Client
from javascript import require

from exceptions.notion import MalformedDatabaseException

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
    return martian.markdownToBlocks(markdown, {"nonInline": "ignore"}).valueOf()


def split_url(url: str):
    """
    The function `split_url` takes a URL as input and returns the value of the query parameter "v" if it
    exists, otherwise it returns None.

    Args:
      url (str): The `url` parameter is a string that represents a URL.

    Returns:
      the captured group from the regular expression match, which is the value between the forward slash
    ("/") and the question mark ("?") followed by "v=". If there is a match, it returns the captured
    group, otherwise it returns None.
    """
    matches = re.search(r"\/(\w+)\?v=", url)
    return matches[1] if matches else None


def write_to_page(page_id: str, blocks: list):
    """
    The function `write_to_page` appends a list of blocks to a Notion page with a given page ID.

    Args:
      page_id (str): The `page_id` parameter is a string that represents the ID of the page in Notion
    where you want to write the blocks to. This ID is typically a unique identifier for the page.
      blocks (list): The `blocks` parameter is a list of blocks that you want to write to a Notion page.
    Each block in the list represents a different type of content that you want to add to the page.
    """
    notion.blocks.children.append(page_id, children=blocks)


def update_status(page: str, status: str):
    """
    The function `update_status` updates the status property of a page in Notion with the provided
    status value.

    Args:
      page (str): The `page` parameter is the identifier of the page you want to update. It could be the
    page ID or the URL of the page.
      status (str): The `status` parameter is a string that represents the new status value that you
    want to update for the given `page`.
    """
    notion.pages.update(
        page,
        properties={
            "Status": {
                "status": {"name": status},
            },
        },
    )


def create_primary_page(database: str, title: str, category: str, icon: str):
    """
    The function `create_primary_page` creates a primary page in Notion with specified properties and
    returns the ID of the created page.

    Args:
      database (str): The `database` parameter is the ID of the database where you want to create the
    primary page. This is typically a string of alphanumeric characters that uniquely identifies the
    database in Notion.
      title (str): The title of the primary page you want to create in Notion.
      category (str): The "category" parameter is a string that represents the category of the primary
    page. It is used to set the value of the "Category" property in the Notion page.
      icon (str): The `icon` parameter is a string representing an emoji that will be used as the icon
    for the primary page.

    Returns:
      the ID of the newly created page in Notion.
    """
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
            "Name": {"title": [{"text": {"content": title}}]},
            "Category": {
                "select": {
                    "name": category,
                },
            },
            "Status": {
                "status": {"name": "In progress"},
            },
        },
    }
    return notion.pages.create(**payload)["id"]


def create_subpage(primary_page: str, title: str, icon: str, content: list | None):
    """
    The `create_subpage` function creates a subpage in Notion with the specified primary page, title,
    icon, and content.

    Args:
      primary_page (str): The primary_page parameter is the ID of the primary page where the subpage
    will be created.
      title (str): The title parameter is a string that represents the title of the subpage.
      icon (str): The "icon" parameter is a string that represents an emoji. It is used to specify the
    icon for the subpage.
      content (list | None): The `content` parameter is a list that represents the content of the
    subpage. Each item in the list represents a block in the subpage. Blocks can be text, headings,
    lists, images, etc. The structure of each block depends on the type of block being used.

    Returns:
      the ID of the newly created subpage.
    """
    payload = {
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
    }

    if content:
        payload["children"] = content

    return notion.pages.create(**payload)["id"]


def get_categories(database_id: str) -> list[str]:
    """
    The function `get_categories` retrieves the list of options for the "Category" property of a Notion
    database.

    Args:
      database_id (str): The `database_id` parameter is a string that represents the ID of the Notion
    database. This ID is unique to each database and can be found in the URL of the Notion page when you
    are viewing the database.

    Returns:
      a list of strings, which represents the options available for the "Category" property in a Notion
    database.
    """
    try:
        return notion.databases.retrieve(database_id)["properties"]["Category"][
            "select"
        ]["options"]
    except KeyError as e:
        raise MalformedDatabaseException(
            "Could not access Category properties, ensure the Notion page is correct schema."
        ) from e


def _random_notion_colour():
    """
    The function `_random_notion_colour` returns a random color from a predefined list.

    Returns:
      The function `_random_notion_colour` returns a randomly chosen color from the list of colors.
    """
    return random.choice(
        [
            "default",
            "gray",
            "brown",
            "orange",
            "yellow",
            "green",
            "blue",
            "pink",
            "purple",
            "red",
        ]
    )


def create_category(database_id: str, category: str):
    """
    The `create_category` function updates a database in Notion by adding a new category option to the
    "Category" property.

    Args:
      database_id (str): The `database_id` parameter is a string that represents the ID of the database
    in which you want to create the category.
      category (str): The `category` parameter is a string that represents the name of the category you
    want to create.

    Returns:
      the result of the `notion.databases.update()` method.
    """
    existing_categories = get_categories(database_id)

    return notion.databases.update(
        database_id,
        properties={
            "Category": {
                "type": "select",
                "select": {
                    "options": [
                        *existing_categories,  # We need to pass the existing categories, as this request would wipe them without them
                        {"name": category, "color": _random_notion_colour()},
                    ],
                },
            },
        },
    )
