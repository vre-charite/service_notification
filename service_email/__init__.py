from flask_restx import Api, Resource, fields
# from flask_restful import Api
module_api = Api(
    version='1.0', 
    title='Email service API',
    description='Email API', 
    doc='/v1/api-doc'
)

# api = Api()
api = module_api.namespace('Email Service', description='Operation on email', path ='/')

# user operations
from service_email.ops_email import WriteEmails
api.add_resource(WriteEmails, '/v1/email')
