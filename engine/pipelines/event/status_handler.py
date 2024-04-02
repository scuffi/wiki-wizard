from datetime import timedelta

from .event_handler import EventHandler

from config.redis import update_status, Status, redis_client
from models import Section

class StatusEventHandler(EventHandler):
    def __init__(self, task_id: str) -> None:
        super().__init__()
        self._task_id = task_id
        
        self.register("onStart", self.on_start)
        self.register("pageSetup", self.on_page_setup)
        self.register("sectionsGenerated", self.on_sections_generated)
        self.register("sectionWritten", self.on_section_write)
        self.register("onComplete", self.on_complete)
        self.register("onFail", self.on_fail)
        
    @property
    def task_id(self):
        return self._task_id
    
    def on_start(self, title: str):
        update_status(self.task_id, Status.PAGE_SETUP)
        redis_client.expire(self.task_id, timedelta(days=3), nx=True)
        
    def on_page_setup(self, title: str, page_id: str):
        update_status(self.task_id, Status.GENERATING_SECTIONS)
        
    def on_sections_generated(self, sections: list):
        update_status(self.task_id, Status.GENERATING_CONTENT)
        
    def on_section_write(self, section: Section, index: int, sections: list[Section]):
        update_status(self.task_id, "Written section " + str(index + 1) + " of " + str(len(sections)))
        
    def on_complete(self, title: str):
        update_status(self.task_id, Status.COMPLETE)
        
    def on_fail(self, title: str, page_id: str):
        update_status(self.task_id, Status.FAILED)
 