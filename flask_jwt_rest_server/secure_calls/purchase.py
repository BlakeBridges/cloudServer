from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
from tools.logging import logger
import jwt
from tools.get_aws_secrets import get_secrets




def handle_request():
    logger.debug("Purchase Handle Request")
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
        token = auth_headers[1]
        logger.debug("Got purchase token")
        secrets = get_secrets()
        decodedJWT = jwt.decode(token, secrets['JWT'], algorithms=["HS256"])
        logger.debug(decodedJWT)
        user_name = decodedJWT['sub']
     
        query = sql.SQL("select * from users where userID = {user_name};").format(
            user_name=sql.Literal(user_name))
        g.cur.execute(query)
        db_user = g.cur.fetchone()[0]
        if(db_user == None):
            logger.debug("user not found")
            return json_response(status_=500, message = 'Could not find user in database', authenticated =  False )
        else:
            logger.debug("In purchase else")
            data = request.get_data()
            book = data.decode("utf-8")
            logger.debug(book)
            query = sql.SQL("insert into purchases values({newPurchase});").format(
                newPurchase=sql.SQL(', ').join([
                    sql.Literal(user_name),
                    sql.Literal(book)]))
            g.cur.execute(query)
            g.db.commit()
            return json_response(status_=200, message = 'Purchase successful', authenticated = True )
    except jwt.ExpiredSignatureError:
             return json_response(status_=401 ,message=expired_msg) # 401 is Unauthorized HTTP status code
    except (jwt.InvalidTokenError, Exception) as e:
            logger.debug(e)
            return json_response(status_=401 ,message=expired_msg)


        
