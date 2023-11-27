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


@dataclass
class Section:
    # This is the actual tree that stores the breakdown of the different headings
    tree: Tree

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
