import unittest
from unittest.mock import patch
from os import path
import os
from requests import HTTPError
import smtplib
from smtplib import SMTP
from app import create_app
from tests.logger import Logger
import base64


class TestWriteEmails(unittest.TestCase):
    log_name = 'test_ops_email.log'
    log = Logger(name=log_name)
    log.warning("Removing old records")
    log.debug("Test is ready to begin")
    post_api = "/v1/email"

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client(self)

    def tearDown(self):
        os.system('rm -rf logs')

    @patch('smtplib.SMTP')
    def test_post_correct(self, mock_smtp):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        self.log.info('\n')
        self.log.info('test post with correct payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_post_no_sender(self, mock_smtp):
        payload = {
            "sender": None,
            "receiver": "jzhang@indocresearch.org",
            "message": "test email"
        }
        self.log.info('\n')
        self.log.info('test post without sender in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {400}")
            self.assertEqual(response.status_code, 400)
            self.log.info(f"COMPARING: {b'missing sender or receiver or message'}")
            self.log.info("IN")
            self.log.info(f"{response.data}")
            assert b"missing sender or receiver or message" in response.data
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_post_no_receiver(self, mock_smtp):
        payload = {
            "sender": "notification@vre",
            "receiver": None,
            "message": "test email"
        }
        self.log.info('\n')
        self.log.info('test post without receiver in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {400}")
            self.assertEqual(response.status_code, 400)
            self.log.info(f"COMPARING: {b'missing sender or receiver or message'}")
            self.log.info("IN")
            self.log.info(f"{response.data}")
            assert b"missing sender or receiver or message" in response.data
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_post_no_message(self, mock_smtp):
        payload = {
            "sender": "notification@vre",
            "receiver": "jzhang@indocresearch.org",
            "message": None
        }
        self.log.info('\n')
        self.log.info('test post without message in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {400}")
            self.assertEqual(response.status_code, 400)
            self.log.info(f"COMPARING: {b'missing sender or receiver or message'}")
            self.log.info("IN")
            self.log.info(f"{response.data}")
            assert b"missing sender or receiver or message" in response.data
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_html_email(self, mock_smtp):
        html_msg = '''<!DOCTYPE html> \
                        <body>\
                        <h4>Dear VRE member,</h4>\
                        </body>\
            </html>'''
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": html_msg,
                   "msg_type": "html"}
        self.log.info('\n')
        self.log.info('test post with html message type in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_wrong_message(self, mock_smtp):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test message",
                   "msg_type": "csv"}
        self.log.info('\n')
        self.log.info('test post with other(csv) message type in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {400}")
            self.assertEqual(response.status_code, 400)
            self.log.info(f"COMPARING: {b'wrong email type'}")
            self.log.info("IN")
            self.log.info(f"{response.data}")
            assert b"wrong email type" in response.data
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_multiple_receiver_list(self, mock_smtp):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org", "jiayu@indocresearch.org"],
                   "message": "test email"}
        self.log.info('\n')
        self.log.info('test post with a list of receivers in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_list_receiver(self, mock_smptp):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        self.log.info('\n')
        self.log.info('test post with receiver in the list format in payload'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_logs(self):
        self.log.info('\n')
        self.log.info('test check if logs directory created'.center(80, '-'))
        self.log.info(f"EXISTS OF LOGS FOLDER: {path.exists('./logs')}")
        self.assertTrue(path.exists('./logs'))

    @patch.object(smtplib, 'SMTP', side_effect=smtplib.socket.gaierror)
    def test_smtp_error(self, mock_smtp_connection_error):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        self.log.info('\n')
        self.log.info('test smtplib.socket.gaierror occurred during posting'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info("MOCK ERROR: smtplib.socket.gaierror")
            self.log.info(f"COMPARING: {response.status_code} VS {500}")
            self.assertEqual(response.status_code, 500)
            self.log.info(f"CHECKING IS NOT NONE: {response.data}")
            self.assertIsNotNone(response.data)
        except Exception as e:
            self.log.error(e)
            raise e

    @unittest.skip("This test does not work with Jenkins")
    @patch.object(SMTP, 'sendmail', side_effect=HTTPError)
    def test_error(self, mock_smtp_send_error):
        payload = {"sender": "notification@vre",
                   "receiver": ["jzhang@indocresearch.org"],
                   "message": "test email"}
        self.log.info('\n')
        self.log.info('test unexpected error(HTTPError) occurred during posting'.center(80, '-'))
        self.log.info(f"POST API: {self.post_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        response = self.app.post(self.post_api, json=payload)
        self.log.info(f"POST RESPONSE: {response}")
        try:
            self.log.info("MOCK ERROR: requests.HTTPError")
            self.log.info(f"COMPARING: {response.status_code} VS {500}")
            self.assertEqual(response.status_code, 500)
            self.log.info(f"CHECKING IS NOT NONE: {response.data}")
            self.assertIsNotNone(response.data)
        except Exception as e:
            self.log.error(e)
            raise e

    @patch('smtplib.SMTP')
    def test_send_email_with_png_attachment(self, mock_smtp):
        self.log.info('\n')
        self.log.info('test send email with attachment'.center(80, '-'))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        png_path = dir_path + "/Testdateiäöüß1.png"
        self.log.info(f"Current directory {dir_path}")
        if not path.isfile(png_path):
            os.system('touch ' + png_path)

        with open(png_path, 'rb') as img:
            payload = {"sender": "notification@vre",
                       "receiver": ["jzhang@indocresearch.org"],
                       "message": "test email",
                       "subject": "test email",
                       "msg_type": "plain",
                       "attachments": [
                           {"name": png_path,"data": base64.b64encode(img.read()).decode('utf-8')}
                       ]
                       }
            self.log.info(f"POST API: {self.post_api}")
            self.log.info(f"POST PAYLOAD: {payload}")
            try:
                response = self.app.post(self.post_api, json=payload)
                self.log.info(f"POST RESPONSE: {response}")
                self.log.info(f"COMPARING: {response.status_code} VS {200}")
                self.assertEqual(response.status_code, 200)
            except Exception as e:
                self.log.error(e)
                raise e
            finally:
                os.system('rm ' + png_path)

    @patch('smtplib.SMTP')
    def test_send_email_with_multiple_attachments(self, mock_smtp):
        self.log.info('\n')
        self.log.info('test send email with multiple attachments'.center(80, '-'))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pdf_path = dir_path + "/Testdateiäöüß2.pdf"
        jpg_path = dir_path + "/Testdateiäöüß3.jpg"
        jpeg_path = dir_path + "/Testdateiäöüß4.jpeg"
        gif_path = dir_path + "/Testdateiäöüß5.gif"
        self.log.info(f"Current directory {dir_path}")
        if not path.isfile(pdf_path) or \
                not path.isfile(jpg_path) or \
                not path.isfile(jpeg_path) or \
                not path.isfile(gif_path):
            os.system('touch ' + pdf_path)
            os.system('touch ' + jpg_path)
            os.system('touch ' + jpeg_path)
            os.system('touch ' + gif_path)

        with open(pdf_path, 'rb') as img1:
            with open(jpg_path, 'rb') as img2:
                with open(jpeg_path, 'rb') as img3:
                    with open(gif_path, 'rb') as img4:
                        payload = {"sender": "notification@vre",
                                   "receiver": ["jzhang@indocresearch.org"],
                                   "message": "test email",
                                   "subject": "test email",
                                   "msg_type": "plain",
                                   "attachments": [
                                       {"name": pdf_path, "data": base64.b64encode(img1.read()).decode('utf-8')},
                                       {"name": jpg_path, "data": base64.b64encode(img2.read()).decode('utf-8')},
                                       {"name": jpeg_path, "data": base64.b64encode(img3.read()).decode('utf-8')},
                                       {"name": gif_path, "data": base64.b64encode(img4.read()).decode('utf-8')}
                                   ]
                                   }
                        self.log.info(f"POST API: {self.post_api}")
                        self.log.info(f"POST PAYLOAD: {payload}")
                        try:
                            response = self.app.post(self.post_api, json=payload)
                            self.log.info(f"POST RESPONSE: {response}")
                            self.log.info(f"COMPARING: {response.status_code} VS {200}")
                            self.assertEqual(response.status_code, 200)
                        except Exception as e:
                            self.log.error(e)
                            raise e
                        finally:
                            os.system('rm ' + pdf_path)
                            os.system('rm ' + jpg_path)
                            os.system('rm ' + jpeg_path)
                            os.system('rm ' + gif_path)

    @patch('smtplib.SMTP')
    def test_send_email_with_unsupport_attachment(self, mock_smtp):
        self.log.info('\n')
        self.log.info('test send email with unsupported attachment'.center(80, '-'))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        xml_path = dir_path + "/Testdateiäöüß1.xml"

        self.log.info(f"Current directory {dir_path}")
        if not path.isfile(xml_path):
            os.system('touch ' + xml_path)

        with open(xml_path, 'rb') as img:
            payload = {"sender": "notification@vre",
                       "receiver": ["jzhang@indocresearch.org"],
                       "message": "test email",
                       "subject": "test email",
                       "msg_type": "plain",
                       "attachments": [
                           {"name": "Testdateiäöüß1.xml", "data": base64.b64encode(img.read()).decode('utf-8')}
                       ]
                       }
            self.log.info(f"POST API: {self.post_api}")
            self.log.info(f"POST PAYLOAD: {payload}")
            try:
                response = self.app.post(self.post_api, json=payload)
                self.log.info(f"POST RESPONSE: {response.data}")
                self.log.info(f"COMPARING: {response.status_code} VS {400}")
                self.assertEqual(response.status_code, 400)
            except Exception as e:
                self.log.error(e)
                raise e
            finally:
                os.system('rm ' + xml_path)

    @patch('smtplib.SMTP')
    def test_send_email_with_large_attachment(self, mock_smtp):
        self.log.info('\n')
        self.log.info('test send email with oversized attachment'.center(80, '-'))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        large_file_path = dir_path + "/Testdateiäöüß_large.pdf"

        self.log.info(f"Current directory {dir_path}")
        if not path.isfile(large_file_path):
            os.system('fallocate -l 2.5M ' + large_file_path)

        with open(large_file_path, 'rb') as img:
            payload = {"sender": "notification@vre",
                       "receiver": ["jzhang@indocresearch.org"],
                       "message": "test email",
                       "subject": "test email",
                       "msg_type": "plain",
                       "attachments": [
                           {"name": "Testdateiäöüß_large.pdf", "data": base64.b64encode(img.read()).decode('utf-8')}
                       ]
                       }
            self.log.info(f"POST API: {self.post_api}")
            self.log.info(f"POST PAYLOAD: {payload}")
            try:
                response = self.app.post(self.post_api, json=payload)
                self.log.info(f"POST RESPONSE: {response.data}")
                self.log.info(f"COMPARING: {response.status_code} VS {413}")
                self.assertEqual(response.status_code, 413)
            except Exception as e:
                self.log.error(e)
                raise e
            finally:
                os.system('rm ' + large_file_path)

