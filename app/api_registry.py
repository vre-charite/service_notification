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

from fastapi import FastAPI

from .routers.v1.api_announcement import api_announcement
from .routers.v1.api_email import api_email
from .routers.v1.api_notification import api_notification


def api_registry(app: FastAPI):
    app.include_router(api_announcement.router, prefix='/v1/announcements', tags=['announcement'])
    app.include_router(api_email.router, prefix='/v1/email', tags=['email'])
    app.include_router(api_notification.router, prefix='/v1/notification', tags=['notification'])
    app.include_router(api_notification.routerBulk, prefix='/v1/notifications', tags=['notification'])
    app.include_router(api_notification.routerUnsub, prefix='/v1/unsubscribe', tags=['notification'])
