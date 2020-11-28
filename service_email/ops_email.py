from flask import request, after_this_request, current_app
from flask_restx import Api, Resource, fields
from config import ConfigClass
from service_email import api
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import smtplib
import os


class WriteEmails(Resource):
    # user login
    # Swagger
    query_payload = api.model(
        "query_payload_basic", {
            "sender": fields.String(readOnly=True, description='sender'),
            "receiver": fields.String(readOnly=True, description='receiver'),
            "message": fields.String(readOnly=True, description='message')
        }
    )
    query_sample_return = '''
    # Below are the sample return
    {
        "result": {"Email sent successfully"}
    }
    '''
    #################################################################
    @api.expect(query_payload)
    @api.response(200, query_sample_return)
    def post(self):
        current_app.logger.info('received request')
        post_data = request.get_json()
        sender = post_data.get('sender', None)
        receiver = post_data.get('receiver', None)
        text = post_data.get('message', None)
        subject = post_data.get('subject', None)
        msg_type = post_data.get('msg_type', 'plain')

        if sender is None or receiver is None or text is None:
            current_app.logger.exception(
                'missing sender or receiver or message')
            return {'result': 'missing sender or receiver or message'}, 400

        current_app.logger.info(f'payload: {post_data}')
        current_app.logger.info(f'receiver: {receiver}')
        try:
            env = os.environ.get('env')
            if env is None or env == 'charite':
                client = smtplib.SMTP(
                    ConfigClass.POSTFIX_URL, ConfigClass.POSTFIX_PORT)
            else:
                client = smtplib.SMTP(
                    ConfigClass.postfix, ConfigClass.smtp_port)
                client.login(ConfigClass.smtp_user, ConfigClass.smtp_pass)

            current_app.logger.info('email server connection established')
        except smtplib.socket.gaierror as e:
            current_app.logger.exception(
                f'Error connecting with Mail host, {e}')
            return {'result': str(e)}, 500

        if not isinstance(receiver, list):
            return {'result': 'receiver must be a list'}, 400

        for to in receiver:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] =  to 
            msg['Subject'] = Header(subject, 'utf-8')

            if msg_type == 'plain':
                msg.attach(MIMEText(text, 'plain', 'utf-8'))
            elif msg_type == 'html':
                msg.attach(MIMEText(text, 'html', 'utf-8'))
            else:
                current_app.logger.exception('wrong email type')
                return {'result': 'wrong email type'}, 400

            try:
                current_app.logger.info(f'message: {msg}')
                client.sendmail(sender, to, msg.as_string())
            except Exception as e:
                current_app.logger.exception(
                    f'Error when sending email to {receiver}, {e}')
                return {'result': str(e)}, 500
        client.quit()
        current_app.logger.info(f'Email sent successfully to {receiver}')
        return {'result': "Email sent successfully. "}, 200
