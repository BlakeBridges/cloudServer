from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from db_con import get_db
from tools.logging import logger


def handle_request():
    logger.debug("Get Books Handle Request")
    global_db_con = get_db()
    cur = global_db_con.cursor()
    cur.execute("select title, author from books;")
    books = cur.fetchall()
    if books == None:
       return json_response(status_=500, message = 'Could not access books database', authenticated =  False )
    else:
     bookList = []
     for book in books:
        bookList.append(book)
    return json_response( token = create_token(  g.jwt_data ) , books = bookList)

