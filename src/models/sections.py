from dataclasses import dataclass
from itertools import groupby
from nutree import Tree


@dataclass(frozen=True)
class Heading:
    index: str
    title: str


@dataclass
class Section:
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

    def get_writable_headings(self):
        """This function returns the lowest in the tree of all the headings, as they are the only that are meant to be written about."""
        return (node.data for node in self.tree if node.is_leaf())


def group_headings(sections: list[Heading]) -> list[list[Heading]]:
    return [list(section) for _, section in groupby(sections, lambda s: s.index[0])]
