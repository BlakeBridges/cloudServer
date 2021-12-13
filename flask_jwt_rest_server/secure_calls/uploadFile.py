from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
from tools.logging import logger
import jwt
from tools.get_aws_secrets import get_secrets
import os
from datetime import date
import subprocess
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])


def CreateNewDir(folder):
    logger.debug("Creating new folder")
    day = date.today()
    dt_string = '{:%d-%m-%Y}'.format(day)
    logger.debug(dt_string)
    newFolder = folder+dt_string
    if not(os.path.isdir(newFolder)):
        os.makedirs(newFolder)
        logger.debug(f"Path {newFolder} created")
    else:
        logger.debug(f"Path {newFolder} already exists")
    return newFolder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_request():
    logger.debug("UploadFile called")
    auth_headers = request.headers.get('Authorization', '').split(':')
    invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
    expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

    if len(auth_headers) != 2:
            return json_response(status_=401 ,message=invalid_msg)


    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
            
                return json_response(status = 412, message = "No files submitted")
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return json_response(status = 415, message = "File type not found.")
            if not allowed_file(file.filename):
                return json_response(status = 415, message = "File type not supported.")
            if file and allowed_file(file.filename):
                logger.debug("File accepted and being processed")
                UPLOAD_FOLDER = './Cloud_Storage/'
                filename = secure_filename(file.filename)
                UPLOAD_FOLDER = CreateNewDir(UPLOAD_FOLDER)
                logger.debug("Trying to save file")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return json_response(status = 200, message = "Successful upload.")
    except jwt.ExpiredSignatureError:
             return json_response(status_=401 ,message=expired_msg) # 401 is Unauthorized HTTP status code
    except (jwt.InvalidTokenError, Exception) as e:
            logger.debug(e)
            return json_response(status_=401 ,message=expired_msg)
 
