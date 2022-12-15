from datetime import datetime
from io import BytesIO
from time import sleep

from pygtail import Pygtail
from minio import Minio
from minio.error import InvalidResponseError

import json


def read_log(tail):
    data = bytearray(b'')
    for line in tail:
        log = json.loads(line)
        data += json.dumps(log, ensure_ascii=False).encode('utf8')
        data += "\n".encode('UTF-8')
    return data

def write_minio(data, minio_client):
    object_name = datetime.now().strftime("%Y-%m-%d_%H-%M") + '.json'
    try:
        minio_client.put_object("log-files",
                                    object_name, 
                                    data=BytesIO(data),
                                    length=len(data), 
                                    content_type='application/json')
        print("File uploaded successfully!")
    except InvalidResponseError as err:
        print(err)



if __name__ == "__main__":

    # Create Minio client
    minio_client = Minio(
        endpoint="localhost:9000",
        secure=False,
        access_key="log-depositor",
        secret_key="minioadmin"
    )

    # Ensure that neccesary bucket exists
    bucket_exists = minio_client.bucket_exists("log-files")
    assert bucket_exists, "'log-files' bucket does not exist"

    tail = Pygtail("log_file.json")

    while True:
        data = bytearray(b'')
        while datetime.now().minute not in list(range(0,60,15)):
            data += read_log(tail)
            sleep(15)
        if data:
            write_minio(data, minio_client)
            sleep(15)
        
