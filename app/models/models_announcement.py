# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from pydantic import BaseModel
from pydantic import Field

from .base_models import APIResponse
from .base_models import PaginationRequest


class GETAnnouncementResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {'content': 'Hello World Again!', 'id': 1, 'project_code': 'hello', 'version': '2.0'},
        },
    )


class GETAnnouncement(PaginationRequest):
    project_code: str
    start_date: str = Field('', example='2021-02-23')
    end_date: str = Field('', example='2021-02-23')
    version: str = ''
    page_size: int = 10
    sorting: str = 'version'


class POSTAnnouncementResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {'content': 'Hello World Again!', 'id': 1, 'project_code': 'hello', 'version': '2.0'},
        },
    )


class POSTAnnouncement(BaseModel):
    project_code: str
    content: str
    publisher: str
