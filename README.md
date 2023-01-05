# ML_Production_Systems

## How to run:
- Start Postgres if not already running:
  - pg_ctl start -D "C:\Program Files\PostgreSQL\15\data"
- Start minio (runs on port 53135):
  - ./minio server minio_data
- start email service (runs on port 8888):
  - POSTGRES_DATABASE=email_ingestion POSTGRES_USERNAME=ingestion_service POSTGRES_PASSWORD='puppet-soil-SWEETEN POSTGRES_HOST=localhost python email_service.py
- Start mailbox service (runs on port 8889):
  - python mailbox_service.py
- Start log collection:
  - MINIO_ACESS_KEY=log-depositor MINIO_SECRET_KEY=minioadmin MINIO_ENDPOINT=localhost:9000 MINIO_BUCKET=log-files LOG_FILE_PATH=./log_file.json python log_collection.py
