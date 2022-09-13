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

import base64
import os
import platform
from os import path

from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.mark.skip()
class TestWriteEmails():
    post_api = '/v1/email/'
    app = TestClient(app)
    TEST_EMAIL_SENDER = 'sender@test.com'
    TEST_EMAIL_RECEIVER = 'receiver@test.com'
    TEST_EMAIL_RECEIVER_2 = 'receiver2@test.com'

    def test_post_correct(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'Test email contents',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 200

    def test_post_no_sender(self):
        payload = {'sender': None, 'receiver': self.TEST_EMAIL_RECEIVER, 'message': 'test email'}
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 422
        assert b'none is not an allowed value' in response.content

    def test_post_no_receiver(self):
        payload = {'sender': self.TEST_EMAIL_SENDER, 'receiver': None, 'message': 'test email'}
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 422
        assert b'none is not an allowed value' in response.content

    def test_post_no_message(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 400
        assert b'Text or template is required' in response.content

    def test_html_email(self):
        html_msg = '''<!DOCTYPE html> \
                        <body>\
                        <h4>Dear member,</h4>\
                        </body>\
            </html>'''
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': html_msg,
            'msg_type': 'html',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 200

    def test_wrong_message(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test message',
            'msg_type': 'csv',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 400
        assert b'wrong email type' in response.content

    def test_multiple_receiver_list(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER, self.TEST_EMAIL_RECEIVER_2],
            'message': 'test email',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 200

    def test_list_receiver(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test email',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 200

    @pytest.mark.skip('Changing logging in progress')
    def test_logs(self):
        self.assertTrue(path.exists('./logs'))

    @pytest.mark.skip('Not working with Pytest yet')
    def test_smtp_error(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test email',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 500
        assert response.content != None

    @pytest.mark.skip('This test does not work with Jenkins')
    def test_error(self):
        payload = {
            'sender': self.TEST_EMAIL_SENDER,
            'receiver': [self.TEST_EMAIL_RECEIVER],
            'message': 'test email',
        }
        response = self.app.post(self.post_api, json=payload)
        assert response.status_code == 500
        assert response.content != None

    def test_send_email_with_png_attachment(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        png_path = dir_path + '/Testdateiäöüß1.png'
        if not path.isfile(png_path):
            os.system('touch ' + png_path)

        with open(png_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [{'name': png_path, 'data': base64.b64encode(img.read()).decode('utf-8')}],
            }
            response = self.app.post(self.post_api, json=payload)
            assert response.status_code == 200
            os.system('rm ' + png_path)

    def test_send_email_with_multiple_attachments(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pdf_path = dir_path + '/Testdateiäöüß2.pdf'
        jpg_path = dir_path + '/Testdateiäöüß3.jpg'
        jpeg_path = dir_path + '/Testdateiäöüß4.jpeg'
        gif_path = dir_path + '/Testdateiäöüß5.gif'
        if (
            not path.isfile(pdf_path)
            or not path.isfile(jpg_path)
            or not path.isfile(jpeg_path)
            or not path.isfile(gif_path)
        ):
            os.system('touch ' + pdf_path)
            os.system('touch ' + jpg_path)
            os.system('touch ' + jpeg_path)
            os.system('touch ' + gif_path)

        with open(pdf_path, 'rb') as img1:
            with open(jpg_path, 'rb') as img2:
                with open(jpeg_path, 'rb') as img3:
                    with open(gif_path, 'rb') as img4:
                        payload = {
                            'sender': self.TEST_EMAIL_SENDER,
                            'receiver': [self.TEST_EMAIL_RECEIVER],
                            'message': 'test email',
                            'subject': 'test email',
                            'msg_type': 'plain',
                            'attachments': [
                                {'name': pdf_path, 'data': base64.b64encode(img1.read()).decode('utf-8')},
                                {'name': jpg_path, 'data': base64.b64encode(img2.read()).decode('utf-8')},
                                {'name': jpeg_path, 'data': base64.b64encode(img3.read()).decode('utf-8')},
                                {'name': gif_path, 'data': base64.b64encode(img4.read()).decode('utf-8')},
                            ],
                        }
                        response = self.app.post(self.post_api, json=payload)
                        assert response.status_code == 200
                        os.system('rm ' + pdf_path)
                        os.system('rm ' + jpg_path)
                        os.system('rm ' + jpeg_path)
                        os.system('rm ' + gif_path)

    def test_send_email_with_unsupport_attachment(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        xml_path = dir_path + '/Testdateiäöüß1.xml'

        if not path.isfile(xml_path):
            os.system('touch ' + xml_path)

        with open(xml_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [{'name': 'Testdateiäöüß1.xml', 'data': base64.b64encode(img.read()).decode('utf-8')}],
            }
            response = self.app.post(self.post_api, json=payload)
            assert response.status_code == 400
            os.system('rm ' + xml_path)

    def test_send_email_with_large_attachment(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        large_file_path = dir_path + '/Testdateiäöüß_large.pdf'

        if not path.isfile(large_file_path):
            if platform.system() == 'Darwin':
                os.system('mkfile -n 2.5M ' + large_file_path)
            else:
                os.system('fallocate -l 2.5M ' + large_file_path)

        with open(large_file_path, 'rb') as img:
            payload = {
                'sender': self.TEST_EMAIL_SENDER,
                'receiver': [self.TEST_EMAIL_RECEIVER],
                'message': 'test email',
                'subject': 'test email',
                'msg_type': 'plain',
                'attachments': [
                    {'name': 'Testdateiäöüß_large.pdf', 'data': base64.b64encode(img.read()).decode('utf-8')}
                ],
            }
            response = self.app.post(self.post_api, json=payload)
            assert response.status_code == 413
            os.system('rm ' + large_file_path)
