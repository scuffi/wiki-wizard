from typing import Annotated
from dataclasses import dataclass, field

from fastapi import FastAPI, Header, BackgroundTasks

from pipelines import CompletePipeline
from config import EnabledModels
from models import ModelConfig

app = FastAPI(title="WikiWizard API")


@dataclass
class GenerateBody:
    title: str
    writing: str = field(default=EnabledModels.WRITING)
    headings: str = field(default=EnabledModels.HEADINGS)
    icons: str = field(default=EnabledModels.ICONS)
    categories: str = field(default=EnabledModels.CATEGORIES)


@app.post("/generate")
def generate_page(
    page_url: Annotated[str, Header()],
    notion_secret: Annotated[str, Header()],
    oai_key: Annotated[str, Header()],
    body: GenerateBody,
    background_tasks: BackgroundTasks,
):
    pipeline = CompletePipeline(
        page_url,
        notion_secret=notion_secret,
        model_config=ModelConfig(
            oai_key=oai_key,
            writing=body.writing,
            headings=body.headings,
            icons=body.icons,
            categories=body.categories,
        ),
    )

    background_tasks.add_task(pipeline.run, body.title)
    return {"message": f"'{body.title}' added to generation queue"}


@app.get("/status/{id}")
def status(id: str):
    ...
