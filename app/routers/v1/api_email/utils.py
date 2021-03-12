from app.config import ConfigClass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ConfigClass.ALLOWED_EXTENSIONS

def is_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ConfigClass.IMAGE_EXTENSIONS
