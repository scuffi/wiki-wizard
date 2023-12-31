import re
from dataclasses import dataclass
from typing import Generator
from itertools import groupby
from nutree import Tree


@dataclass(unsafe_hash=True)
class Heading:
    index: str  # The index of this heading, e.g '3.5.1' as a string
    title: str  # The title of this heading, e.g. '20th Century Cars'
    content: str | None = (
        None  # The content of this heading, may be None if no content generated yet
    )

    def has_content(self):
        return self.content is not None


@dataclass
class Section:
    # This is the actual tree that stores the breakdown of the different headings
    tree: Tree

    @classmethod
    def from_string(cls, value: str) -> list["Section"]:
        """Convert an LLM output/response into a list of parsed Sections.

        This utilises static regex & other functions so the output should be predictable based on when it was written.

        Args:
            response (str): The plaintext response.

        Returns:
            list[Section]: Aggregated and ordered Sections.
        """
        pattern = re.compile(r"(\d+(\.\d+)*)\s*:\s*(.*)")
        matches = pattern.findall(value)

        # Turn the text into groups of headings, called Sections
        headings = group_headings(
            [Heading(index=match[0], title=match[2].strip()) for match in matches]
        )

        # Create 'n' amount of Tree objects
        trees = [Section(Tree()) for _ in range(len(headings))]

        # Iterate over everything, and add each heading to the respective tree
        for i, section in enumerate(headings):
            last_index = ""
            last_node = trees[i].tree

            stack = [last_node]

            for heading in section:
                if heading.index.count(".") > last_index.count("."):
                    stack.append(last_node)
                    last_node = last_node.add(heading)
                    last_index = heading.index
                    continue

                if heading.index.count(".") < last_index.count("."):
                    stack.pop()

                last_node = stack[-1].add(heading)
                last_index = heading.index

        return trees

    def format(self) -> str:
        """Formats this section into a human-readable list.

        Example:
        ```text
        6: Consumer Choices and Trends
            6.1: Brand Selection
                6.1.1: Market Leaders
                6.1.2: Niche Brands and Products
            6.2: Price Points and Accessibility
                6.2.1: Premium vs. Budget-Friendly Options
                6.2.2: Global Availability and Local Preferences
            6.3: Marketing and Advertising Strategies
                6.3.1: Target Demographics
                6.3.2: Claims and Endorsements
                6.3.3: Social Media and Influencer Marketing
        ```

        Returns:
            str: The multiline list as a string
        """
        result = [
            f"{'    '*heading.data.index.count('.')}{heading.data.index}: {heading.data.title}"
            for heading in self.tree
        ]
        return "\n".join(result)

    def get_writable_headings(self) -> Generator[Heading, None, None]:
        """This function returns the lowest in the tree of all the headings, as they are the only that are meant to be written about."""
        return (node.data for node in self.tree if node.is_leaf())

    def dump(self):
        """Convert the given section into a string complete with content."""
        lines = []
        for node in self.tree:
            heading = node.data
            lines.append(
                f"{'#'*heading.index.count('.')} {heading.index}: {heading.title}"
            )

            if heading.has_content():
                lines.append(heading.content)

        return "\n".join(lines)


def group_headings(sections: list[Heading]) -> list[list[Heading]]:
    """Create nested lists for each group of headings.
    A group is determined by the predominant number, for example, 1, 1.2, 1.3.4, etc are all grouped together.

    Note: Sections must be sorted and in increasing order when passed in.

    Args:
        sections (list[Heading]): A list of every section in order.

    Returns:
        list[list[Heading]]: A list of sublists containing ordered groups of headings.
    """
    return [list(section) for _, section in groupby(sections, lambda s: s.index[0])]
