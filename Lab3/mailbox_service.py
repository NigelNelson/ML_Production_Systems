# Authors: Nigel Nelson, Collin Quinn
# Assignment: Project #2
# Course: ML Production
# Date: 1/3/23

from flask import Flask
import structlog


app = Flask(__name__)


def configure(log_fl):
  """
  Reusable code in GET, PUT, DELETE routes 
  """
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
  with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
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
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="email::id::folder::get",
              email_id=email_id,
              )
    
    return {
      "folder": "Inbox"
    }


@app.route('/mailbox/email/<email_id>/labels', methods=['GET'])
def get_email_labels(email_id):
  """
  Returns a JSON object with the fields "email_id" and "labels".  The value for labels is a list of strings.  Valid labels include "spam", "read", and "important".  No label may be repeated.
  """
  with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
    configure(log_fl)
    logger = structlog.get_logger()
    logger.info(event="email::id::labels::get",
            email_id=email_id,
            )

  return {
    "email_id": email_id,
    "labels": ["read", "important"]
  }


@app.route('/mailbox/folder/<folder>', methods=['GET'])
def get_emails_by_folder(folder):
    """
    Lists the emails in a given folder.  Returns a list of email_ids.
    """
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="folder::emails::get",
                  folder=folder,
                  )

    return {
      "email_ids": [1,2,3,4]
    }


@app.route('/mailbox/labels/<label>', methods=['GET'])
def get_emails_by_label(label):
    """
    List emails with the given label.  Returns a list of email_ids.
    """
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="labels::label::get",
                  label=label,
                  )

    return {
      'email_ids' : [1,2,3]
    }


@app.route('/mailbox/email/<email_id>/folder/<folder>', methods=['PUT'])
def put_email_to_folder(email_id, folder):
    """
    Moves email to the given folder.  Folders include "Inbox", "Archive", "Trash", and "Sent".
    """
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="email::id::folder::folder::put",
                  email_id=email_id,
                  folder=folder
                  )

    return {
      'folder' : 'Inbox'
    }


@app.route('/mailbox/email/<email_id>/label/<label>', methods=['PUT'])
def mark_email_with_label(email_id, label):
    """
    Mark the given email with the given label. Valid labels include "spam", "read", and "important".
    """
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="email::id::label::put",
                  email_id=email_id,
                  label=label
                  )

    return {
      'label' : 'read'
    }


@app.route('/mailbox/email/<email_id>/label/<label>', methods=['DELETE'])
def remove_label_from_email(email_id, label):
    """
    Remove the given label from the given email. Valid labels include "spam", "read", and "important".
    """
    with open("log_file.json", "a", encoding="utf-8") as log_fl:
    
      configure(log_fl)
      logger = structlog.get_logger()
      logger.info(event="email::id::label::delete",
                  email_id=email_id,
                  label=label
                  )

    return {
      'label': 'read'
    }


app.run(port=8889)
