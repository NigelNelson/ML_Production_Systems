import os
from io import BytesIO
import json
import pickle
import sys
from datetime import datetime
import pandas as pd
from minio import Minio
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

if not len(sys.argv) == 3:
    print('Missing config params .json file or minio bucket argument')
    sys.exit(1)

config_file = sys.argv[1] # Collect config file name
email_bucket = sys.argv[2] # Collect email bucket name

# Collect env vars to connect to Minio
MINIO_ACESS_KEY = os.environ.get('MINIO_ACESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')

# Exit if environment variable missing
if not MINIO_ACESS_KEY or not MINIO_SECRET_KEY \
   or not MINIO_ENDPOINT:
    print('One of the environment variables (ACESS_KEY/SECRET_KEY/ENDPOINT/) \
         is missing')
    sys.exit(1)

# Create Minio client
minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    secure=False, # allow HTTP
    access_key=MINIO_ACESS_KEY,
    secret_key=MINIO_SECRET_KEY
)

# Create list of .json files in specified Minio bucket
files = minio_client.list_objects(email_bucket, recursive=True)
json_files = [object.object_name for object in list(filter(lambda file: '.json' in file.object_name , files))]

# Parse all .json files and append to a list contatining all json objects
email_dicts = []
for file in json_files:
    with minio_client.get_object(email_bucket, file) as response:
        json_str = response.data.decode('utf-8')
        for line in json_str.split('\n')[:-1]: # indexing removes last invalid empty string
            data = json.loads(line)
            email_json = json.loads(data['email_object'])
            email_json['label'] = data['label']
            email_json['received_timestamp'] = data['received_timestamp']
            email_dicts.append(email_json)

# Create DataFrame from the list of json objects
email_df = pd.DataFrame.from_dict(email_dicts)
email_df['label'] = email_df['label'].astype('category')

# Collect the json config
with open(config_file, 'r') as f:
    config = json.load(f)
# Convert ngram_range to tuple so constructor accepts the arg
config['vect_params']['ngram_range'] = tuple(config['vect_params']['ngram_range'])

# Create CountVectorizer using config params
vectorizer = CountVectorizer(**config['vect_params'])

X_train = vectorizer.fit_transform(email_df['body'])
y_train = email_df['label'].to_numpy()

# Create LogisticRegression using config params
reg = LogisticRegression(**config['reg_params'])

# Train LogisticRegression on all emails
reg.fit(X_train, y_train)

# Gather meta data to be saved in pickle file
email_df.sort_values(by='received_timestamp', ascending=True)
meta_data = {
    'value_counts': email_df['label'].value_counts().to_dict(),
    'earliest_email': email_df.iloc[0]['received_timestamp'],
    'latest_email': email_df.iloc[-1]['received_timestamp'],
    'config_params': config
}


output_pkl = {'reg':reg,
              'vect': vectorizer, 
              'meta_data': meta_data
              }     
object_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.json'
pickle_obj = pickle.dumps(output_pkl)

# Save output pickle file to 'models' Minio bucket
minio_client.put_object('models',
                            object_name, 
                            data=BytesIO(pickle_obj),
                            length=len(pickle_obj)
                            )