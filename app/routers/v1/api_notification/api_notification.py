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
from datetime import timezone

from fastapi import APIRouter
from fastapi import Depends
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from logger import LoggerFactory

from app.models.base_models import EAPIResponseCode
from app.models.models_notification import DELETENotification
from app.models.models_notification import DELETENotificationResponse
from app.models.models_notification import GETNotification
from app.models.models_notification import GETNotificationResponse
from app.models.models_notification import GETNotifications
from app.models.models_notification import POSTNotification
from app.models.models_notification import POSTNotificationResponse
from app.models.models_notification import PUTNotification
from app.models.models_notification import PUTNotificationResponse
from app.models.models_unsub import POSTUnsub
from app.models.models_unsub import POSTUnsubResponse
from app.models.sql_notification import NotificationModel
from app.models.sql_notification import UnsubscribedModel
from app.routers.v1.router_utils import paginate

router = APIRouter()
routerBulk = APIRouter()
routerUnsub = APIRouter()
_logger = LoggerFactory('api_notification').get_logger()


@cbv(router)
class APINotification:
    @router.get('/', response_model=GETNotificationResponse, summary='Query one maintenance notification by ID')
    async def get_notification(self, params: GETNotification = Depends(GETNotification)):
        try:
            api_response = GETNotificationResponse()
            notification = db.session.query(NotificationModel).filter_by(id=params.id)
            api_response.page = 0
            api_response.num_of_pages = 1
            api_response.total = 1
            api_response.result = notification.first().to_dict()
        except Exception as e:
            readable_error = f'Could not get notification with id={params.id}'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.post('/', response_model=POSTNotificationResponse, summary='Create new maintenance notification')
    async def create_notification(self, data: POSTNotification):
        api_response = POSTNotificationResponse()
        if len(data.message) > 250:
            api_response.set_error_msg('Message too long')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        if int(data.detail.duration) <= 0:
            api_response.set_error_msg('Duration less than or equal to zero')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        model_data = {
            'type': data.type,
            'message': data.message,
            'maintenance_date': data.detail.maintenance_date,
            'duration': data.detail.duration,
            'duration_unit': data.detail.duration_unit,
            'created_date': str(datetime.now(timezone.utc)),
        }
        notification = NotificationModel(**model_data)
        try:
            db.session.add(notification)
            db.session.commit()
            db.session.refresh(notification)
            api_response.result = notification.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.put('/', response_model=PUTNotificationResponse, summary='Modify one maintenance notification by ID')
    async def modify_notification(self, id: int, data: PUTNotification):
        api_response = PUTNotificationResponse()
        if len(data.message) > 250:
            api_response.set_error_msg('Message too long')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        if int(data.detail.duration) <= 0:
            api_response.set_error_msg('Duration less than or equal to zero')
            api_response.set_code(EAPIResponseCode.bad_request)
            return api_response.json_response()
        try:
            notification = db.session.query(NotificationModel).filter_by(id=id).first()
            notification.type = data.type
            notification.message = data.message
            notification.created_date = str(datetime.now(timezone.utc))
            notification.maintenance_date = data.detail.maintenance_date
            notification.duration = data.detail.duration
            notification.duration_unit = data.detail.duration_unit
            db.session.commit()
            db.session.refresh(notification)
            api_response.result = notification.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()

    @router.delete('/', response_model=DELETENotificationResponse, summary='Delete one maintenance notification by ID')
    async def delete_notification(self, params: DELETENotification = Depends(DELETENotification)):
        api_response = DELETENotificationResponse()
        try:
            notification = db.session.query(NotificationModel).filter_by(id=params.id)
            db.session.delete(notification.first())
            db.session.commit()
        except Exception as e:
            readable_error = 'Failed to delete from database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()


@cbv(routerBulk)
class APINotificationBulk:
    @routerBulk.get('/', response_model=GETNotificationResponse, summary='Query many maintenance notifications')
    async def get_all_notifications(self, params: GETNotifications = Depends(GETNotifications)):
        api_response = GETNotificationResponse()
        notifications = db.session.query(NotificationModel).order_by(NotificationModel.created_date.desc())
        if not params.all:
            if not params.username:
                api_response.error_msg = 'Username must be provided if all is false'
                api_response.code = EAPIResponseCode.bad_request
                return api_response.json_response()
            unsubs = db.session.query(UnsubscribedModel).filter_by(username=params.username).all()
            unsubNotificationIds = []
            for unsub in unsubs:
                unsubNotificationIds.append(unsub.notification_id)
            notifications = notifications.filter(NotificationModel.id.not_in(unsubNotificationIds))
        paginate(params, api_response, notifications)
        return api_response.json_response()


@cbv(routerUnsub)
class APINotificationUnsub:
    @routerUnsub.post(
        '/', response_model=POSTUnsubResponse, summary='Unsubscribe one user from one maintenance notification'
    )
    async def unsub_notification(self, data: POSTUnsub):
        api_response = POSTUnsubResponse()
        model_data = {'username': data.username, 'notification_id': data.notification_id}
        unsub = UnsubscribedModel(**model_data)
        try:
            db.session.add(unsub)
            db.session.commit()
            db.session.refresh(unsub)
            api_response.result = unsub.to_dict()
        except Exception as e:
            readable_error = 'Failed to write to database'
            _logger.exception(f'{readable_error}\n{e}')
            api_response.set_error_msg(readable_error)
            api_response.set_code(EAPIResponseCode.bad_request)
        return api_response.json_response()
