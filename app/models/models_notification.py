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

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from .base_models import APIResponse


# GET
class GETNotificationResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'page': 0,
            'total': 1,
            'num_of_pages': 1,
            'result': {
                'type': 'maintenance',
                'message': 'Notification response message',
                'created_date': '2022-01-01 12:00:00.000000',
                'detail': {
                    'maintenance_date': '2022-01-01 12:00:00.000000',
                    'duration': '3',
                    'duration_unit': 'h',
                },
            },
        },
    )


class GETNotifications(BaseModel):
    all: bool = True
    page_size: int = 10
    page: int = 0
    username: str = None


class GETNotification(BaseModel):
    id: int


# POST
class POSTNotificationResponse(GETNotificationResponse):
    pass


class POSTNotificationDetail(BaseModel):
    maintenance_date: datetime
    duration: int
    duration_unit: str


class POSTNotification(BaseModel):
    type: str
    message: str
    detail: POSTNotificationDetail


# PUT
class PUTNotificationResponse(POSTNotificationResponse):
    pass


class PUTNotification(POSTNotification):
    pass


# DELETE
class DELETENotificationResponse(APIResponse):
    result: dict = Field(
        {},
        example={
            'code': 200,
            'error_msg': '',
            'result': {
                'id': 1,
                'status': 'success',
            },
        },
    )


class DELETENotification(BaseModel):
    id: int
