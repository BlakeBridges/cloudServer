from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
import bcrypt
from tools.logging import logger


def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    username_from_user_form = request.form['username']
    password_from_user_form = request.form['password']
    user = {
            "sub" : username_from_user_form #sub is used by pyJwt as the owner of the token
            }
    if not user:
        return json_response(status_=401, message = 'No username was input', authenticated =  False )
    query = sql.SQL( "select passhash from users where userID = {user_name};").format(
            user_name=sql.Literal(username_from_user_form))
    g.cur.execute(query)
    db_pass = g.cur.fetchone()[0]
    if(db_pass == None):
        return json_response(status_=401, message = 'User not found in system', authenticated =  False )
    else:
        db_pass = bytes(db_pass, 'utf-8')
        checkPass = bcrypt.checkpw(bytes(password_from_user_form, 'utf-8'), db_pass)
        if(checkPass):
           return json_response(token = create_token(user) , authenticated = True)
        
        return json_response(status_=401, message = 'Passwords do not match', authenticated =  False )

