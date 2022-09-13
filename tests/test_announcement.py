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

from fastapi.testclient import TestClient

from app.main import app


class TestAnnouncement:
    app = TestClient(app)

    def test_01_post_announcement(self):
        payload = {
            'project_code': 'test_01',
            'content': 'Content for test announcement',
            'publisher': 'erik'
        }
        response = self.app.post('/v1/announcements/', json=payload)
        assert response.status_code == 200
    
    def test_02_get_announcements(self):
        params = {
            'project_code': 'test_01',
            'order': 'asc',
            'version': '1'
        }
        response = self.app.get('/v1/announcements/', params=params)
        assert response.status_code == 200
    
    def test_03_post_announcements_message_too_long(self):
        payload = {
            'project_code': 'test_03',
            'content': 'Content for test announcement with a long message. Rem omnis ea sit. Aliquam omnis tempora est aliquam illo laborum. Mollitia voluptatem deserunt dolorem sapiente ad fugit minima tenetur. Atque qui corporis rerum veritatis aut. Et consectetur aut corporis earum cumque inventore occaecati rerum.',
            'publisher': 'erik'
        }
        response = self.app.post('/v1/announcements/', json=payload)
        assert response.status_code == 400
    
    def test_04_get_announcements_no_end_date(self):
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01'
        }
        response = self.app.get('/v1/announcements/', params=params)
        assert response.status_code == 400
    
    def test_05_get_announcements_desc(self):
        params = {
            'project_code': 'test_01',
            'order': 'desc'
        }
        response = self.app.get('/v1/announcements/', params=params)
        assert response.status_code == 200
    
    def test_06_get_announcements_with_dates(self):
        params = {
            'project_code': 'test_01',
            'start_date': '2022-01-01',
            'end_date': '2022-12-31'
        }
        response = self.app.get('/v1/announcements/', params=params)
        assert response.status_code == 200
