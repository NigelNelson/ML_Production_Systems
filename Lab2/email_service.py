# Authors: Nigel Nelson, Collin Quinn
# Assignment: Project #2
# Course: ML Production
# Date: 1/3/23

from flask import Flask, request, jsonify
import json, random
import psycopg2
import os
import sys
from datetime import datetime, timezone


app = Flask(__name__)


def get_db_connection():
    """
    Returns connection to the database specified by supplied
    environment variables
    """

    POSTGRES_DATABASE=os.environ.get('POSTGRES_DATABASE')
    POSTGRES_USERNAME=os.environ.get('POSTGRES_USERNAME')
    POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOST=os.environ.get('POSTGRES_HOST')

    # Exit if environment variable missing
    if not POSTGRES_DATABASE or not POSTGRES_USERNAME \
       or not POSTGRES_PASSWORD or not POSTGRES_HOST:
        print('One of the environment variables (DATABASE/USERNAME/HOST/PASSWORD) is missing')
        sys.exit(1)

    conn = psycopg2.connect(host=POSTGRES_HOST,
                            database=POSTGRES_DATABASE,
                            user=POSTGRES_USERNAME,
                            password=POSTGRES_PASSWORD)

    return conn


@app.route('/email', methods=['POST'])
def post_email():
    """
    Email endpoint that converts the email to a json object and stores
    it in the specified database
    """

    email_id = random.randint(1000, 9999)
    dt = datetime.now(timezone.utc)

    request_data = request.get_json()
    request_data_to = request_data["to"]
    request_data_from = request_data["from"]
    request_data_subject = request_data["subject"]
    request_data_body = request_data["body"]

    body = {
            "to": request_data_to,
            "from": request_data_from,
            "subject": request_data_subject,
            "body": request_data_body
    }

    json_body = json.dumps(body).replace(r'\u0000', '')
   
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails (received_timestamp, email_object) VALUES (%s, %s)',
                    (dt, json_body))
    

    # ------------ For verification -----------
    # postgreSQL_select_Query = "select * from emails"

    # cursor.execute(postgreSQL_select_Query)
    # records = cursor.fetchall()
    # for row in records:
    #     print(row)
    # --------------------------
    
    conn.commit()
    cursor.close()

    return jsonify(email_id=email_id)


conn = get_db_connection()
app.run(port=8888)

    