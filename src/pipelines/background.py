from tasks import notion, categoriser, icons, headings, writing, WritingMethod


class BackgroundPipeline:
    def __init__(self, notion_page_url: str) -> None:
        self._database = notion.split_url(notion_page_url)

    def _get_category(self, title: str) -> str:
        """
        The function `_get_category` retrieves the category of a given title from a database, creates the
        category if it doesn't exist, and returns the category.

        Args:
          title (str): The `title` parameter in the `_get_category` method is a string that represents the
        title of a category.

        Returns:
          a string, which is the category of the given title.
        """
        categories = notion.get_categories(self._database)
        category = categoriser.find_category(title, [cat["name"] for cat in categories])

        if category not in [cat["name"] for cat in categories]:
            notion.create_category(self._database, category)

        return category

    def _setup_page(self, title: str, category: str) -> str:
        """
        The `_setup_page` function creates a primary page in a Notion database with a given title, category,
        and icon, and writes default content to the page including a table of contents and a divider.

        Args:
          title (str): The `title` parameter is a string that represents the title of the page that will be
        created.
          category (str): The "category" parameter is a string that represents the category of the page. It
        is used as a parameter when creating the primary page in the `create_primary_page` function.

        Returns:
          The function `_setup_page` returns the `page_id` as a string.
        """
        page_id = notion.create_primary_page(
            self._database,
            title=title,
            category=category,
            icon=icons.generate_icon(title),
        )

        # Write the defaults to the page
        notion.write_to_page(
            page_id,
            [
                {
                    "type": "table_of_contents",
                    "table_of_contents": {"color": "default"},
                },
                {"type": "divider", "divider": {}},
            ],
        )

        return page_id

    def _iterate_sections(self, page_id: str, title: str):
        """
        The `_iterate_sections` function iterates through sections and headings, creates subpages for leaf
        nodes, and writes content for non-leaf nodes.

        Args:
          page_id (str): The `page_id` parameter is a string that represents the ID of a page in the Notion
        database. It is used to identify the page where the sections will be created or updated.
          title (str): The `title` parameter in the `_iterate_sections` method is a string that represents
        the title of a page.
        """
        sections = headings.generate_headings(title)

        for section in sections:
            for node in section.tree:
                heading = node.data

                if node.is_leaf():
                    written_section = writing.write_section(
                        section=section,
                        heading=heading,
                        title=title,
                        method=WritingMethod.SINGLE,
                    )
                    heading.content = written_section
                    parsed = notion.parse_to_notion(written_section)

                    notion.create_subpage(
                        page_id,
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

                    notion.write_to_page(page_id, content)

        notion.update_status(page_id, "Done")

    def _create_sections(self, page_id: str, title: str):
        """
        The function `_create_sections` is responsible for iterating through sections and updating the
        status of a page in a Notion database.

        Args:
          page_id (str): The `page_id` parameter is a string that represents the unique identifier of a page
        in the Notion database. It is used to identify the page where the sections will be created.
          title (str): The `title` parameter is a string that represents the title of a page.
        """
        # TODO: Change this into a handler per section/subheading, that way we can skip or write an error if something breaks instead of halting entire program
        try:
            self._iterate_sections(page_id, title)
        except Exception as ex:
            notion.update_status(page_id, "Failed")
            raise ex

    def run(self, title: str):
        """
        The `run` function takes a `title` as input, retrieves the `category` based on the title, sets up a
        page with the given title and category, and creates sections for the page.

        Args:
          title (str): The `title` parameter is a string that represents the title of a page.
        """
        category = self._get_category(title)
        page_id = self._setup_page(title, category)
        self._create_sections(page_id, title)