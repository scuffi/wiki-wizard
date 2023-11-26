from dataclasses import dataclass
from itertools import groupby


@dataclass
class Heading:
    index: str
    title: str


@dataclass
class Section:
    headings: list[Heading]


def group_sections(sections: list[Heading]) -> list[Section]:
    return [
        Section(list(section)) for _, section in groupby(sections, lambda s: s.index[0])
    ]
