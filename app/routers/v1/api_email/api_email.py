from fastapi import APIRouter
from fastapi_utils import cbv
from fastapi.templating import Jinja2Templates
import jinja2
import base64
import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from multiprocessing import Process
import smtplib

from services.service_logger.logger_factory_service import SrvLoggerFactory
from app.config import ConfigClass
from app.models.models_email import POSTEmail, POSTEmailResponse
from app.models.base_models import EAPIResponseCode
from .utils import allowed_file, is_image

router = APIRouter()
_logger = SrvLoggerFactory('api_emails').get_logger()

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

        _logger.info('email server connection established')
    except smtplib.socket.gaierror as e:
        _logger.exception(
            f'Error connecting with Mail host, {e}')
        api_response.result = str(e)
        api_response.code = EAPIResponseCode.internal_error
        return api_response.json_response()

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
            _logger.info(f"\nto: {to}\nfrom: {sender}\nsubject: {msg['Subject']}")
            print(msg)
            client.sendmail(sender, to, msg.as_string())
        except Exception as e:
            _logger.exception(
                f'Error when sending email to {to}, {e}')
            api_response.result = str(e)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
    client.quit()


@cbv.cbv(router)
class WriteEmails:

    @router.post('/', response_model=POSTEmailResponse, summary="Send emails")
    async def post(self, data: POSTEmail):
        api_response = POSTEmailResponse()
        templates = Jinja2Templates(directory="emails")
        text = data.message
        template = data.template

        if text and template:
            api_response.result = 'Please only set text or template, not both'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        if not text and not template:
            _logger.exception('Text or template is required')
            api_response.result = 'Text or template is required'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        if template:
            try:
                template = templates.get_template(data.template)
                text = template.render(data.template_kwargs)
            except jinja2.exceptions.TemplateNotFound as e:
                api_response.result = 'Template not found'
                api_response.code = EAPIResponseCode.not_found
                return api_response.json_response()

        attachments = []
        for file in data.attachments:
            if "," in file.get("data"):
                attach_data = base64.b64decode(file.get("data").split(",")[1])
            else:
                attach_data = base64.b64decode(file.get("data"))

            # check if bigger to 2mb
            if len(attach_data) > 2000000:
                api_response.result = 'attachement to large'
                api_response.code = EAPIResponseCode.to_large
                return api_response.json_response()

            filename = file.get("name")
            if not allowed_file(filename):
                api_response.result = 'File type not allowed'
                api_response.code = EAPIResponseCode.bad_request
                return api_response.json_response()

            if attach_data and allowed_file(filename):
                if is_image(filename):
                    attach = MIMEImage(attach_data)
                    attach.add_header('Content-Disposition', 'attachment', filename=filename)
                else:
                    attach = MIMEApplication(attach_data, _subtype='pdf', filename=filename)
                    attach.add_header('Content-Disposition', 'attachment', filename=filename)
                attachments.append(attach)

        if data.msg_type not in ['html', 'plain']:
            api_response.result = 'wrong email type'
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        log_data = data.__dict__.copy()
        if log_data.get("attachments"):
            del log_data["attachments"]
        _logger.info(f'payload: {log_data}')
        _logger.info(f'receiver: {data.receiver}')

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

            _logger.info('email server connection established')
        except smtplib.socket.gaierror as e:
            api_response.result = str(e)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
        client.quit()

        p = Process(
            target=send_emails,
            args=(data.receiver, data.sender, data.subject, text, data.msg_type, attachments),
        )
        p.daemon = True
        p.start()
        _logger.info(f'Email sent successfully to {data.receiver}')
        api_response.result = "Email sent successfully. "
        return api_response.json_response()
