from dataclasses import dataclass, field
from config import EnabledModels


@dataclass
class Model:
    key: str
    model: str
    temperature: float = field(default=0)


@dataclass
class ModelConfig:
    oai_key: str
    writing: str = field(default=EnabledModels.WRITING)
    headings: str = field(default=EnabledModels.HEADINGS)
    icons: str = field(default=EnabledModels.ICONS)
    categories: str = field(default=EnabledModels.CATEGORIES)
