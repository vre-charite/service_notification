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

import time

from fastapi import APIRouter
from fastapi import Depends
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError

from app.models.base_models import EAPIResponseCode
from app.models.models_announcement import GETAnnouncement
from app.models.models_announcement import GETAnnouncementResponse
from app.models.models_announcement import POSTAnnouncement
from app.models.models_announcement import POSTAnnouncementResponse
from app.models.sql_announcement import AnnouncementModel
from app.routers.v1.router_utils import paginate

router = APIRouter()


@cbv(router)
class APIAnnouncement:
    @router.get('/', response_model=GETAnnouncementResponse, summary='Query all announcements for project')
    async def get_announcements(self, params: GETAnnouncement = Depends(GETAnnouncement)):
        api_response = GETAnnouncementResponse()

        if params.start_date and not params.end_date or params.end_date and not params.start_date:
            api_response.error_msg = 'Both start_date and end_date need to be supplied'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        query_data = {
            'project_code': params.project_code,
        }
        if params.version:
            query_data['version'] = params.version

        if params.sorting:
            if params.order == 'asc':
                sort_param = getattr(AnnouncementModel, params.sorting).asc()
            else:
                sort_param = getattr(AnnouncementModel, params.sorting).desc()
            announcements = db.session.query(AnnouncementModel).filter_by(**query_data).order_by(sort_param)
        else:
            sort_param = getattr(AnnouncementModel, params.sorting).asc()
            announcements = db.session.query(AnnouncementModel).filter_by(**query_data).order_by(sort_param)

        if params.start_date and params.end_date:
            announcements = announcements.filter(
                AnnouncementModel.date >= params.start_date, AnnouncementModel.date <= params.end_date
            )
        paginate(params, api_response, announcements)
        return api_response.json_response()

    @router.post('/', response_model=POSTAnnouncementResponse, summary='Create new announcement')
    async def create_announcement(self, data: POSTAnnouncement):
        api_response = POSTAnnouncementResponse()

        if len(data.content) > 250:
            api_response.error_msg = 'Content to long'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        model_data = {
            'project_code': data.project_code,
            'version': str(time.time()),
            'content': data.content,
            'publisher': data.publisher,
        }
        announcement = AnnouncementModel(**model_data)
        try:
            db.session.add(announcement)
            db.session.commit()
            db.session.refresh(announcement)
        except IntegrityError:
            api_response.set_error_msg('project_code and version already exist in db')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.to_dict, api_response.code
        api_response.result = announcement.to_dict()
        return api_response.json_response()
