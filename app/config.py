import os 

class ConfigClass(object):
    # the packaged modules
    env = os.environ.get('env')
    api_modules = ["service_email"]
    postfix = 'mailout.easydns.com'
    smtp_user = 'oit.on.ca'
    smtp_pass = '1991alex'
    smtp_port = 587

    POSTFIX_URL = "external-postfix.utility"
    POSTFIX_PORT = 25

    ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    version = "1.1.0"

    RDS_HOST = "opsdb.utility"
    RDS_PORT = "5432"
    RDS_DBNAME = "INDOC_VRE"
    RDS_USER = "postgres"
    RDS_PWD = "postgres"
    if env == 'charite':
        RDS_USER = "indoc_vre"
        RDS_PWD = os.environ.get('RDS_PWD')
    RDS_SCHEMA_DEFAULT = "indoc_vre"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USER}:{RDS_PWD}@{RDS_HOST}/{RDS_DBNAME}"

