from typing import Annotated
from uuid import uuid4
from dataclasses import dataclass, field
from rich import print

from fastapi import FastAPI, Header, BackgroundTasks
from fastapi.responses import JSONResponse

from pipelines import CompletePipeline, StatusEventHandler
from config import EnabledModels
from config.redis import redis_client
from models import ModelConfig

__version__ = "0.0.2"

app = FastAPI(title="WikiWizard API")

print(f"Starting up... (version: {__version__})")

@app.on_event("startup")
def on_startup():
    print(f"Running version [bold green]{__version__}[/bold green]")


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
    task_id = uuid4().hex
    
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
        event_handler=StatusEventHandler(task_id), # Allow for decoupled Redis status updating
    )

    background_tasks.add_task(pipeline.run, body.title)
    
    return {"message": f"'{body.title}' added to generation queue", "id": task_id}


@app.get("/status/{id}")
def status(id: str):
    if not redis_client.exists(id):
        return JSONResponse(status_code=404, content={"message": "Process not found"})
    
    return JSONResponse(status_code=200, content={"message": redis_client.get(id)})

@app.get("/status")
def status_list():
    keys = redis_client.keys(pattern="generation:*")
    statuses = [redis_client.hget(key, "status") for key in keys]
    return [{"id": key, "status": value} for key, value in zip(keys, statuses)]

