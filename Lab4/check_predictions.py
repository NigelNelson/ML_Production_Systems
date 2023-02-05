
import sys
import os
import json
from minio import Minio

MINIO_ACCESS_KEY=os.environ.get('MINIO_ACESS_KEY')
MINIO_SECRET_KEY=os.environ.get('MINIO_SECRET_KEY')
MINIO_ENDPOINT=os.environ.get('MINIO_ENDPOINT')
MINIO_BUCKET=os.environ.get('MINIO_BUCKET')
LOG_FILE_PATH=os.environ.get('LOG_FILE_PATH')

if not len(sys.argv) == 2:
    print('Missing Minio log file name')
    sys.exit(1)

log_file = sys.argv[1] # Collect Minio log file

minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    secure=False, # allow HTTP
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY
)

# Collect all logs from .json file
json_logs = []
with open(LOG_FILE_PATH, 'r') as file:
    for line in file.readlines():
        json_logs.append(json.loads(line))

# Collect all logs from Minio
minio_logs = []
with minio_client.get_object(bucket_name=MINIO_BUCKET, object_name=log_file) as response:
    json_str = response.data.decode('utf-8')
    for line in json_str.split('\n')[:-1]: # indexing removes last invalid empty string
        data = json.loads(line)
        minio_logs.append(data)

# Filter down lists to only spam labels
json_pos_labels = list(filter(lambda log: log['label'] == 'spam', json_logs))
minio_pos_labels = list(filter(lambda log: log['label'] == 'spam', minio_logs))

json_count = len(json_logs)
minio_count = len(minio_logs)
json_pos_count = len(json_pos_labels)
minio_pos_count = len(minio_pos_labels)

if json_count == minio_count and \
    json_pos_count == minio_pos_count:
    print(f'{LOG_FILE_PATH} and Minio agree:')
    print(f'Total emails: {json_count}')
    print(f'Total spam emails predicted: {json_pos_count}')
    print(f'Total ham emails predicted: {json_count - json_pos_count}')
else:
    print(f'{LOG_FILE_PATH} and Minio Disagree:')
    print(f'Total json emails: {json_count}')
    print(f'Total json spam emails predicted: {json_pos_count}')
    print(f'Total json ham emails predicted: {json_count - json_pos_count}')
    print(f'Total Minio emails: {minio_count}')
    print(f'Total Minio spam emails predicted: {minio_pos_count}')
    print(f'Total Minio ham emails predicted: {minio_count - minio_pos_count}')