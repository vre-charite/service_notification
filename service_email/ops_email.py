from flask import request, after_this_request, current_app
from flask_restx import Api, Resource, fields
from config import ConfigClass
from service_email import api
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from multiprocessing import Process
import requests
import smtplib
import os
import base64
from utils import allowed_file, is_image

def send_emails(receivers, sender, subject, text, msg_type, attachments):
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

    for to in receivers:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] =  to 
        msg['Subject'] = Header(subject, 'utf-8')
        for attachment in attachments:
            msg.attach(attachment)

        if msg_type == 'plain':
            msg.attach(MIMEText(text, 'plain', 'utf-8'))
        else:
            msg.attach(MIMEText(text, 'html', 'utf-8'))

        try:
            current_app.logger.info(f"\nto: {to}\nfrom: {sender}\nsubject: {msg['Subject']}")
            client.sendmail(sender, to, msg.as_string())
        except Exception as e:
            current_app.logger.exception(
                f'Error when sending email to {to}, {e}')
            return {'result': str(e)}, 500
    client.quit()


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
        files = post_data.get('attachments', [])
        attachments = []
        for file in files:
            if "," in file.get("data"):
                data = base64.b64decode(file.get("data").split(",")[1])
            else:
                data = base64.b64decode(file.get("data")) 

            # check if bigger to 2mb
            if len(data) > 2000000:
                return {'result': 'attachment to large'}, 413

            filename = file.get("name")
            if not allowed_file(filename):
                return {'result': 'File type not allowed'}, 400

            if data and allowed_file(filename):
                if is_image(filename):
                    attach = MIMEImage(data)
                    attach.add_header('Content-Disposition', 'attachment', filename=filename)
                else:
                    attach = MIMEApplication(data, _subtype='pdf', filename=filename)
                    attach.add_header('Content-Disposition', 'attachment', filename=filename)
                attachments.append(attach)
        
        if sender is None or receiver is None or text is None:
            current_app.logger.exception(
                'missing sender or receiver or message')
            return {'result': 'missing sender or receiver or message'}, 400

        if msg_type not in ['html', 'plain']:
            current_app.logger.exception('wrong email type')
            return {'result': 'wrong email type'}, 400

        log_data = post_data.copy()
        if log_data.get("attachments"):
            del log_data["attachments"]
        current_app.logger.info(f'payload: {log_data}')
        current_app.logger.info(f'receiver: {receiver}')

        if not isinstance(receiver, list):
            return {'result': 'receiver must be a list'}, 400

        # Open the SMTP connection just to test that it's working before doing the real sending in the background

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
        client.quit()

        p = Process(target=send_emails, args=(receiver, sender, subject, text, msg_type, attachments))
        p.daemon = True
        p.start()
        current_app.logger.info(f'Email sent successfully to {receiver}')
        return {'result': "Email sent successfully. "}, 200
