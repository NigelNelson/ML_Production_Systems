from flask import Flask, request
import sys
from minio import Minio
import pickle
import os
from datetime import datetime
import io
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

app = Flask(__name__)

# given_model_path = sys.argv[1]
# print(given_model_path)

# Collect supplied environment variables
# MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
# MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
# MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
# MINIO_BUCKET = os.environ.get('MINIO_BUCKET')
# LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH')

# for manual testing
MINIO_ACCESS_KEY = "log-depositor"
MINIO_SECRET_KEY = "minioadmin"
MINIO_ENDPOINT = "localhost:9000"
MINIO_BUCKET = "pickel-model"
LOG_FILE_PATH = "./log_file.json"

# Exit if environment variable missing
if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY \
        or not MINIO_ENDPOINT or not MINIO_BUCKET \
        or not LOG_FILE_PATH:
    print('One of the environment variables (ACCESS_KEY/SECRET_KEY/ENDPOINT/BUCKET/LOG_PATH) \
             is missing')
    sys.exit(1)

# Create Minio client
minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    secure=False,  # allow HTTP
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY
)

# Ensure that necessary bucket exists
bucket_exists = minio_client.bucket_exists(MINIO_BUCKET)
assert bucket_exists, f'{MINIO_BUCKET} bucket does not exist'

# https://www.appsloveworld.com/coding/python3x/134/write-a-pickle-file-in-to-minio-object-storage
model = pickle.loads(minio_client.get_object(bucket_name=MINIO_BUCKET, object_name="model.pkl").read())

# Example
# string = ["YOU'VE SEEN IT BEFORE YOU SAY?...\n\nTarget sym: CDYV, Price (current): $0.089, 5 Day Target "
#                   "price: $0.425, Action: Strong Buy/Hold!\n\nSOMEBODY KNOWS SOMETHING..\n\nSee bullish news online "
#                   "right now, the00, call broker.\n\n"]


@app.route('/classify', methods=['GET'])
def classify_email():
    request_data = request.get_json()
    request_data_email_object = request_data['email']
    request_data_email_object_body = str(request_data_email_object['body'])

    object_name = datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json'
    transformer = pickle.loads(minio_client.get_object(bucket_name=MINIO_BUCKET, object_name="vectorizer.pkl").read())
    string_transformed = transformer.transform(request_data_email_object_body)
    result = model.predict(string_transformed)[0]

    if result == 'spam':
        minio_client.put_object(
            MINIO_BUCKET, object_name, io.BytesIO(b'spam'), 4,
        )

    if result == 'ham':
        minio_client.put_object(
            MINIO_BUCKET, object_name, io.BytesIO(b'ham'), 3,
        )

    return {
        "predicted_class": result
    }


app.run(port=8888)
