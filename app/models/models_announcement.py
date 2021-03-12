from enum import Enum
from pydantic import BaseModel, Field
from .base_models import APIResponse, PaginationRequest


class GETAnnouncementResponse(APIResponse):
    result: dict = Field({}, example={
         "code": 200,
        "error_msg": "",
        "page": 0,
        "total": 1,
        "num_of_pages": 1,
        "result": {
          'content': 'Hello World Again!',
          'id': 1,
          'project_code': 'hello',
          'version': '2.0'
        }
    })


class GETAnnouncement(PaginationRequest):
    project_code: str
    start_date: str = Field("", example="2021-02-23")
    end_date: str = Field("", example="2021-02-23")
    version: str = ""
    page_size: int = 10
    sorting: str = "version"


class POSTAnnouncementResponse(APIResponse):
    result: dict = Field({}, example={
         "code": 200,
        "error_msg": "",
        "page": 0,
        "total": 1,
        "num_of_pages": 1,
        "result": {
          'content': 'Hello World Again!',
          'id': 1,
          'project_code': 'hello',
          'version': '2.0'
        }
    })


class POSTAnnouncement(BaseModel):
    project_code: str
    content: str
    publisher: str
