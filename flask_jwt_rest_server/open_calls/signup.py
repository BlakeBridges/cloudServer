from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    #use data here to insert user into DB and auth the user
    username_from_user_form = request.form['username']
    password_from_user_form = request.form['password']
    global_db_con = get_db() 
    
    if not username_from_user_form:
        return json_response(status_=401, message = 'No Username input', authenticated =  False )
    cur = global_db_con.cursor()
    query = sql.SQL( "select * from users where userID = {user_name};").format(
            user_name=sql.Literal(username_from_user_form))
    cur.execute(query)
    nameCheck = cur.fetchone()
    if nameCheck == None:
        salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(12))
        decryptSalt = salted.decode('utf-8')
        logger.debug(decryptSalt)
        query = sql.SQL("insert into users  values({newUser});").format(
                newUser=sql.SQL(', ').join([
                    sql.Literal(username_from_user_form),
                    sql.Literal(decryptSalt)]))
        cur.execute(query)
        global_db_con.commit()
        user = {
                "sub" : username_from_user_form #sub is used by pyJwt as the owner of the token
                }
        return json_response(token = create_token(user) , authenticated = False)
    else:
        return json_response(status_=401, message = 'User Already Exists', authenticated =  False )
