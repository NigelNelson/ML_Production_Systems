# Authors: Nigel Nelson, Collin Quinn
# Assignment: Project #2
# Course: ML Production
# Date: 1/3/23

from datetime import datetime
from io import BytesIO
from time import sleep

from pygtail import Pygtail
from minio import Minio
from minio.error import InvalidResponseError

import json
import os
import sys

def read_log(tail):
    """
    Reads in each new line in the file being tailed, and
    returns a byte array representation.
    """
    data = bytearray(b'')
    for line in tail:
        log = json.loads(line)
        data += json.dumps(log, ensure_ascii=False).encode('utf8')
        data += "\n".encode('UTF-8')
    return data

def write_minio(data, minio_client, bucket):
    """
    Writes the supplied data as a .json file to the supplied
    bucket
    """
    object_name = datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json'
    try:
        minio_client.put_object(bucket,
                                object_name, 
                                data=BytesIO(data),
                                length=len(data), 
                                content_type='application/json')
        print(f'File {object_name} uploaded successfully!')
    except InvalidResponseError as err:
        print(err)
        sys.exit(1)


def main():
    
    # Collect supplied environment variables
    MINIO_ACCESS_KEY=os.environ.get('MINIO_ACESS_KEY')
    MINIO_SECRET_KEY=os.environ.get('MINIO_SECRET_KEY')
    MINIO_ENDPOINT=os.environ.get('MINIO_ENDPOINT')
    MINIO_BUCKET=os.environ.get('MINIO_BUCKET')
    LOG_FILE_PATH=os.environ.get('LOG_FILE_PATH')

    # Exit if environment variable missing
    if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY \
       or not MINIO_ENDPOINT or not MINIO_BUCKET \
        or not LOG_FILE_PATH:
        print('One of the environment variables (ACESS_KEY/SECRET_KEY/ENDPOINT/BUCKET/LOG_PATH) \
             is missing')
        sys.exit(1)

    # Create Minio client
    minio_client = Minio(
        endpoint=MINIO_ENDPOINT,
        secure=False, # allow HTTP
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY
    )

    # Ensure that neccesary bucket exists
    bucket_exists = minio_client.bucket_exists(MINIO_BUCKET)
    assert bucket_exists, f'{MINIO_BUCKET} bucket does not exist'

    # tail the log file
    tail = Pygtail(LOG_FILE_PATH)

    # Loop infinitely
    while True:
        # Write new lines to a byte array and every 15 minutes if
        # the byte array is not empty, write the data to Minio
        data = bytearray(b'')
        while datetime.now().minute not in list(range(0,60,15)):
            data += read_log(tail)
            sleep(15)
        if data:
            write_minio(data, minio_client, MINIO_BUCKET)
            sleep(15)

if __name__ == "__main__":
    main()
