from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
from tools.logging import logger


def handle_request():
    logger.debug("Purchase Handle Request")
    passedJWT = request.form['jwt']
    book = request.form['book']
    decodedJWT = jwt.decode(passedJWT, JWT_SECRET, algorithms=["HS256"])
    print(decodedJWT)
    user_name = decodedJWT['username']
    cur = global_db_con.cursor()
    query = sql.SQL("select * from users where userID = {user_name};").format(
            user_name=sql.Literal(user_name))
    cur.execute(query)
    db_user = cur.fetchone()[0]
    if(db_user == None):
        return json_response(status_=500, message = 'Could not find user in database', authenticated =  False )
    else:
        query = sql.SQL("insert into purchases values({newPurchase});").format(
                newPurchase=sql.SQL(', ').join([
                    sql.Literal(user_name),
                    sql.Literal(book)]))
        cur.execute(query)
        global_db_con.commit()
        return json_response(status_=200, message = 'Purchase successful', authenticated =  False )


        
