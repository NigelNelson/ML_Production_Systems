from datetime import datetime
from io import BytesIO
from time import sleep

from pygtail import Pygtail
from minio import Minio
from minio.error import InvalidResponseError

import json
import os



def read_log(tail):
    data = bytearray(b'')
    for line in tail:
        log = json.loads(line)
        data += json.dumps(log, ensure_ascii=False).encode('utf8')
        data += "\n".encode('UTF-8')
    return data

def write_minio(data, minio_client, bucket):
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



if __name__ == "__main__":

    MINIO_ACESS_KEY=os.environ.get('MINIO_ACESS_KEY')
    MINIO_SECRET_KEY=os.environ.get('MINIO_SECRET_KEY')
    MINIO_ENDPOINT=os.environ.get('MINIO_ENDPOINT')
    MINIO_BUCKET=os.environ.get('MINIO_BUCKET')
    LOG_FILE_PATH=os.environ.get('LOG_FILE_PATH')

    # Create Minio client
    minio_client = Minio(
        endpoint=MINIO_ENDPOINT,
        secure=False,
        access_key=MINIO_ACESS_KEY,
        secret_key=MINIO_SECRET_KEY
    )

    # Ensure that neccesary bucket exists
    bucket_exists = minio_client.bucket_exists(MINIO_BUCKET)
    assert bucket_exists, f'{MINIO_BUCKET} bucket does not exist'

    # tail the log file
    tail = Pygtail(LOG_FILE_PATH)

    while True:
        data = bytearray(b'')
        while datetime.now().minute not in list(range(0,60,15)):
            data += read_log(tail)
            sleep(15)
        if data:
            write_minio(data, minio_client, MINIO_BUCKET)
            sleep(15)
        
