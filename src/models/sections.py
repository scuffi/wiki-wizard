from dataclasses import dataclass
from itertools import groupby


@dataclass
class Section:
    index: str
    title: str


def group_sections(sections: list[Section]) -> list[list[Section]]:
    return [list(section) for _, section in groupby(sections, lambda s: s.index[0])]
