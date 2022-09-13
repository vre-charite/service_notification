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

from json import loads

import pytest
from fastapi.testclient import TestClient

from app.main import app

notificationId = None


class TestNotification():
    app = TestClient(app)

    @pytest.mark.dependency(name='test_01')
    def test_01_post_notification(self):
        payload = {
            'type': 'test_01',
            'message': 'Test message from post',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        global notificationId
        notificationId = loads(response.text)['result']['id']
        assert response.status_code == 200
    
    @pytest.mark.dependency(depends=['test_01'])
    def test_02_get_notification(self):
        params = {'id': notificationId}
        response = self.app.get('/v1/notification/', params=params)
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_03_put_notification(self):
        params = {'id': notificationId}
        payload = {
            'type': 'test_03',
            'message': 'Test message from put',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_04_get_notifications(self):
        response = self.app.get('/v1/notifications/')
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['test_01'])
    def test_05_delete_notification(self):
        params = {'id': notificationId}
        response = self.app.delete('/v1/notification/', params=params)
        assert response.status_code == 200

    @pytest.mark.dependency(name='test_06')
    def test_06_unsubscribe(self):
        payload = {
            'username': 'erik',
            'notification_id': 1,
        }
        response = self.app.post('/v1/unsubscribe/', json=payload)
        assert response.status_code == 200

    def test_07_get_notification_not_exist(self):
        params = {'id': '99999'}
        response = self.app.get('/v1/notification/', params=params)
        assert response.status_code == 400
    
    def test_08_post_notification_message_too_long(self):
        payload = {
            'type': 'test_08',
            'message': 'Test message from post with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        assert response.status_code == 400

    def test_09_post_notification_duration_not_positive(self):
        payload = {
            'type': 'test_09',
            'message': 'Test message from post with an invalid duration',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': -1, 'duration_unit': 'h'},
        }
        response = self.app.post('/v1/notification/', json=payload)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_10_put_notification_message_too_long(self):
        params = {'id': notificationId}
        payload = {
            'type': 'test_10',
            'message': 'Test message from put with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': 1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_01'])
    def test_11_put_notification_duration_not_positive(self):
        params = {'id': notificationId}
        payload = {
            'type': 'test_11',
            'message': 'Test message from put',
            'detail': {'maintenance_date': '2022-01-20T15:20:13.955Z', 'duration': -1, 'duration_unit': 'h'},
        }
        response = self.app.put('/v1/notification/', params=params, json=payload)
        assert response.status_code == 400

    def test_12_get_notifications_no_username(self):
        params = {'all': False}
        response = self.app.get('/v1/notifications/', params=params)
        assert response.status_code == 400

    @pytest.mark.dependency(depends=['test_06'])
    def test_13_get_notifications_with_username(self):
        params = {
            'all': False,
            'username': 'erik'
        }
        response = self.app.get('/v1/notifications/', params=params)
        assert response.status_code == 200
