from pydantic import BaseModel, Field
from app.models.base_models import APIResponse


class POSTEmail(APIResponse):
    sender: str
    receiver: list 
    subject: str = ""
    message: str = ""
    template: str = ""
    template_kwargs: dict = {} 
    msg_type: str = "plain"
    attachments: list = []

class POSTEmailResponse(APIResponse):
    result: str = "success"
