from flask import Flask, request, jsonify, Response
import json, random
import psycopg2
import os
import sys
from datetime import datetime, timezone
import structlog

app = Flask(__name__)


def configure_loging():

  with open("log_file.json", "wt", encoding="utf-8") as log_fl:
    structlog.configure(
      processors=[structlog.processors.TimeStamper(fmt="iso"),
      structlog.processors.JSONRenderer()],
      logger_factory=structlog.WriteLoggerFactory(file=log_fl)
    )


def get_db_connection():
    """
    TODO - read in using environment variables
    """

    # # try: 
    # POSTGRES_DATABASE=os.environ.get('POSTGRES_DATABASE')
    # POSTGRES_USERNAME=os.environ.get('POSTGRES_USERNAME')
    # POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
    # POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
    # # except:
    # #     print('One of the environment variables (DATABASE/USERNAME/HOST/PASSWORD) is missing')
    # #     sys.exit(1)

    # conn = psycopg2.connect(host=POSTGRES_HOST,
    #                         database=POSTGRES_DATABASE,
    #                         user=POSTGRES_USERNAME,
    #                         password=POSTGRES_PASSWORD)

    conn = psycopg2.connect(host='localhost',
                            database='email_ingestion',
                            user='ingestion_service',
                            password='puppet-soil-SWEETEN')

    return conn


@app.route('/email', methods=['POST'])
def post_email():

    conn = psycopg2.connect(host='localhost',
                                database='email_ingestion',
                                user='ingestion_service',
                                password='puppet-soil-SWEETEN',
                                port='5432')
                                
    print(conn)

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

    json_body = json.dumps(body)
   
    # Insert into psql
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
    conn.close()

    return jsonify(email_id=email_id)


@app.route('/mailbox/email/<email_id:int>', methods=['GET'])
def get_email_by_id():
    """
    Returns a JSON object with the key "email" and an associated value of a String containing the entire email text
    """
    
    logger = structlog.get_logger()
    logger.info(event="email::id::get",
                email_id="todo")

    return {
        "email": {
            "to": "",
            "from": "",
            "subject": "",
            "body": ""
        }
    }



# @app.route('/mailbox/email/<email_id:int>/folder', methods=['GET'])
# def get_email_folder():
#     """
#     Get the folder containing the given email.  Examples of folders include "Inbox", "Archive", "Trash", and "Sent".
#     """




# @app.route('/mailbox/email/<email_id:int>/labels', methods=['GET'])
# def get_email_labels():
#     """
#     Returns a JSON object with the fields "email_id" and "labels".  The value for labels is a list of strings.  Valid labels include "spam", "read", and "important".  No label may be repeated.
#     """




# @app.route('/mailbox/folder/<folder:str>', methods=['GET'])
# def get_mailbox_folder():
#     """
#     Lists the emails in a given folder.  Returns a list of email_ids.
#     """



# @app.route('/mailbox/labels/<label:str>', methods=['GET'])
# def get_mailbox_labels():
#     """
#     List emails with the given label.  Returns a list of email_ids.
#     """




# @app.route('/mailbox/email/<email_id:int>/folder/<folder:str>', methods=['PUT'])
# def put_email_to_folder():
#     """
#     Moves email to the given folder.  Folders include "Inbox", "Archive", "Trash", and "Sent".
#     """




# @app.route('/mailbox/email/<email_id:int>/label/<label:str>', methods=['PUT'])
# def mark_email_with_label():
#     """
#     Mark the given email with the given label. Valid labels include "spam", "read", and "important".
#     """




# @app.route('/mailbox/email/<email_id:int>/label/<label:str>', methods=['DELETE'])
# def remove_label_from_email():
#     """
#     Remove the given label from the given email. Valid labels include "spam", "read", and "important".
#     """

configure_loging()
app.run()

# Test connection
# print(get_db_connection())
    