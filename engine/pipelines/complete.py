from nutree import Node
import multiprocessing as mp
from langchain.globals import set_verbose
from rich import print

from config import Prompts
from models import Section, ModelConfig, Model
from tasks import NotionWiki, writing, WritingMethod, generate
from .event.event_handler import EventHandler


class CompletePipeline:
    def __init__(
        self,
        notion_page_url: str,
        notion_secret: str,
        model_config: ModelConfig,
        concurrency: int = 5,
        event_handler: EventHandler = EventHandler(),
    ) -> None:
        self.notion = NotionWiki(notion_secret)
        self._database = self.notion.split_url(notion_page_url)
        self._concurrency = concurrency
        self._handler = event_handler
        self._model_config = model_config

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
        categories = self.notion.get_categories(self._database)
        category = generate.prompt(
            prompt=title,
            system_message=Prompts.categoriser_prompt,
            model=Model(
                key=self._model_config.oai_key,
                model=self._model_config.categories,
            ),
            categories=", ".join([cat["name"] for cat in categories]),
        )

        if category not in [cat["name"] for cat in categories]:
            self.notion.create_category(self._database, category)

        self._handler.fire("categoryFound", category)

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
        page_id = self.notion.create_primary_page(
            self._database,
            title=title,
            category=category,
            icon=generate.prompt(
                prompt=title,
                system_message=Prompts.icons_prompt,
                model=Model(
                    key=self._model_config.oai_key,
                    model=self._model_config.icons,
                    temperature=0.9,
                ),
            ),
        )

        # Write the defaults to the page
        self.notion.write(
            page_id,
            [
                {
                    "type": "table_of_contents",
                    "table_of_contents": {"color": "default"},
                },
                {"type": "divider", "divider": {}},
            ],
        )

        self._handler.fire("pageSetup", title, page_id)

        return page_id

    def _generate_content(self, sections: list[Section], title: str):
        """
        The function `_write_leaves` iterates through a list of sections and their headings, writes the
        content of each section using a specified writing method, and updates the content of each heading
        with the written section.

        Args:
          sections (list[Section]): A list of Section objects. Each Section object represents a section of
        content.
          title (str): The `title` parameter is a string that represents the title of the document or
        section being written.
        """
        pool = mp.Pool(self._concurrency)

        print(
            f"[bold grey]Writing sections for [bold green]{title}[/bold green][/bold grey]"
        )
        for section in sections:
            results = pool.map(
                writing.write_section_mp,
                [
                    (
                        section.format(),
                        heading,
                        title,
                        WritingMethod.SINGLE,
                        self._model_config,
                    )
                    for heading in section.get_writable_headings()
                ],
            )

            for heading, result in zip(section.get_writable_headings(), results):
                heading.content = result

            self._handler.fire("sectionGenerated", section)

        self._handler.fire("sectionsGenerated", sections)

        pool.close()
        pool.join()
        print(
            ":white_check_mark:",
            f"[bold green]Finished writing sections for [bold green]{title}[/bold green][/bold green]",
        )

    def _write_content_to_notion(self, node: Node, page_id: str):
        """
        The `_write_heading` function writes a heading to a Notion page, creating a subpage if the heading
        is a leaf node.

        Args:
          node (Node): The `node` parameter is of type `Node` and represents a node in a tree structure. It
        likely contains data related to a specific section or heading.
          page_id (str): The `page_id` parameter is the unique identifier of the page where the content will
        be written. It is used to specify the destination page for creating subpages or writing content.
          section (Section): The `section` parameter is an object of the `Section` class. It represents a
        section within a page or document.
          title (str): The `title` parameter is a string that represents the title of the section or
        heading.
        """
        try:
            heading = node.data

            if node.is_leaf():
                parsed = self.notion.md_to_blocks(heading.content)

                self.notion.create_subpage(
                    page_id,
                    title=heading.title,
                    icon=generate.prompt(
                        prompt=heading.title,
                        system_message=Prompts.icons_prompt,
                        model=Model(
                            key=self._model_config.oai_key,
                            model=self._model_config.icons,
                            temperature=0.9,
                        ),
                    ),
                    content=parsed,
                )
            else:
                # * Only write title in case we don't create page > should this be configurable
                content = self.notion.md_to_blocks(
                    # f"#{'#'*heading.index.count('.')} {heading.index} - {heading.title}" # ? MAke this configurable option
                    f"#{'#'*heading.index.count('.')} {heading.title}"
                )
                self.notion.write(page_id, content)

            self._handler.fire("headingSave", heading, page_id)
            print(f"[green]Saved '{heading.index}: {heading.title}' to page.[/green]")
        except Exception as ex:
            content = self.notion.md_to_blocks(f"❌ ERROR: {heading.title} ❌ - {ex}")
            try:
                self.notion.write(page_id, content)
            except Exception:
                self._write_content_to_notion(node, page_id)
            self._handler.fire("headingFail", heading, page_id)

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
        sections = Section.from_string(
            generate.prompt(
                prompt=title,
                system_message=Prompts.heading_prompt,
                model=Model(
                    key=self._model_config.oai_key,
                    model=self._model_config.headings,
                ),
            )
        )
        
        self._handler.fire("sectionsGenerated", sections)

        self._generate_content(sections, title)

        for index, section in enumerate(sections):
            for node in section.tree:
                self._write_content_to_notion(
                    node=node,
                    page_id=page_id,
                )
                
                self._handler.fire("sectionWritten", section=section, index=index, sections=sections)

        self.notion.update_status(page_id, "Done")

    def _create_sections(self, page_id: str, title: str):
        """
        The function `_create_sections` is responsible for iterating through sections and updating the
        status of a page in a Notion database.

        Args:
          page_id (str): The `page_id` parameter is a string that represents the unique identifier of a page
        in the Notion database. It is used to identify the page where the sections will be created.
          title (str): The `title` parameter is a string that represents the title of a page.
        """
        try:
            self._iterate_sections(page_id, title)
        except Exception as ex:
            self._handler.fire("onFail", title, page_id)
            self.notion.update_status(page_id, "Failed")
            raise ex

    def run(self, title: str):
        """
        The `run` function takes a `title` as input, retrieves the `category` based on the title, sets up a
        page with the given title and category, and creates sections for the page.

        Args:
          title (str): The `title` parameter is a string that represents the title of a page.
        """
        # TODO: Add a debug mode, where we print more to terminal
        set_verbose(False)  # * Stop langchain printing every output to terminal
        print(f"Starting generation of {title}")
        
        self._handler.fire("onStart", title)
        
        category = self._get_category(title)
        page_id = self._setup_page(title, category)
        self._create_sections(page_id, title)
        self._handler.fire("onComplete", title)
        print(
            ":white_check_mark:",
            f"[bold green]Completed wiki page: '{title}'[/bold green]",
        )
