from flask import Flask, request, jsonify, Response
import json, random
app = Flask(__name__)


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
    