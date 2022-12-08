from flask import Flask, request, jsonify, Response
import json, random
import psycopg2
import os
import sys
from datetime import datetime, timezone
import structlog

app = Flask(__name__)


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


def configure(log_fl):
  
  structlog.configure(
      processors=[structlog.processors.TimeStamper(fmt="iso"),
      structlog.processors.JSONRenderer()],
      logger_factory=structlog.WriteLoggerFactory(file=log_fl)
    )


@app.route('/mailbox/email/<email_id>', methods=['GET'])
def get_email_by_id(email_id):
  """
  Returns a JSON object with the key "email" and an associated value of a String containing the entire email text
  """
  with open("log_file.json", "wt", encoding="utf-8") as log_fl:
    
    configure(log_fl)
    logger = structlog.get_logger()
    logger.info(event="email::id::get",
              email_id=email_id)

  return {
      "email": {
          "to": "smith@msoe.edu",
          "from": "quinnc@msoe.edu",
          "subject": "Please read",
          "body": "body of email"
      }
  }


@app.route('/mailbox/email/<email_id>/folder', methods=['GET'])
def get_email_folder(email_id):
    """
    Get the folder containing the given email.  Examples of folders include "Inbox", "Archive", "Trash", and "Sent".
    """
    with open("log_file.json", "wt", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()

      folder = "Inbox" ## hardcode in folder
      logger.info(event="email::id::folder::get",
              email_id=email_id,
              folder=folder)
    
    return {
      "folder": "Inbox"
    }


@app.route('/mailbox/email/<email_id>/labels', methods=['GET'])
def get_email_labels(email_id):
  """
  Returns a JSON object with the fields "email_id" and "labels".  The value for labels is a list of strings.  Valid labels include "spam", "read", and "important".  No label may be repeated.
  """
  with open("log_file.json", "wt", encoding="utf-8") as log_fl:
    
    configure(log_fl)
    logger = structlog.get_logger()

    logger.info(event="email::id::labels::get",
            email_id=email_id,
            labels=["read", "important"])


  return {
    "email_id": 1,
    "labels": ["read", "important"]
  }


@app.route('/mailbox/folder/<folder>', methods=['GET'])
def get_mailbox_folder(folder):
    """
    Lists the emails in a given folder.  Returns a list of email_ids.
    """

    return {
      "email_ids": [1,2,3,4]
    }



@app.route('/mailbox/labels/<label>', methods=['GET'])
def get_mailbox_labels(label):
    """
    List emails with the given label.  Returns a list of email_ids.
    """


    return {
      'email_ids' : [1,2,3]
    }


@app.route('/mailbox/email/<email_id>/folder/<folder>', methods=['PUT'])
def put_email_to_folder(email_id, folder):
    """
    Moves email to the given folder.  Folders include "Inbox", "Archive", "Trash", and "Sent".
    """

    return {
      'folder' : 'Inbox'
    }


@app.route('/mailbox/email/<email_id>/label/<label>', methods=['PUT'])
def mark_email_with_label(email_id, label):
    """
    Mark the given email with the given label. Valid labels include "spam", "read", and "important".
    """


    return {
      'label' : 'read'
    }


@app.route('/mailbox/email/<email_id>/label/<label>', methods=['DELETE'])
def remove_label_from_email(email_id, label):
    """
    Remove the given label from the given email. Valid labels include "spam", "read", and "important".
    """



    return {
      'label': 'read'
    }

# configure_logging()
conn = get_db_connection()
app.run()

    