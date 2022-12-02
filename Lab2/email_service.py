from flask import Flask, request, jsonify, Response
import json, random
import psycopg2
import os
import sys



app = Flask(__name__)


def get_db_connection():

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
    
    request_data = request.get_json()
    request_data_to = request_data["to"]
    request_data_from = request_data["from"]
    request_data_subject = request_data["subject"]
    request_data_body = request_data["body"]

    int_random = random.randint(1000, 9999)

    return jsonify(email_id=int_random)


app.run(port=5000)
# print(get_db_connection())
    