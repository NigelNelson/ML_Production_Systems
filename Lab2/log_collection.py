#from pygtail import Pygtail
from minio import Minio


client = Minio(
        "http://localhost:9000 ",
        access_key="log-depositor",
        secret_key="minioadmin",
    )


found = client.bucket_exists("log-files")
if not found:
    print("connected")
else:
    print("not connected")
# for line in Pygtail("log_file.json"):
#     sys.stdout.write(line)