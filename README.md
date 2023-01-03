# ML_Production_Systems

## How to run:
- Start Postgres if not already running:
  - pg_ctl start -D "C:\Program Files\PostgreSQL\15\data"
- start email service:
  - POSTGRES_DATABASE=email_ingestion POSTGRES_USERNAME=ingestion_service POSTGRES_PASSWORD='puppet-soil-SWEETEN POSTGRES_HOST=127.0.0.1 python email_service.py
- Start log collection:
  - MINIO_ACESS_KEY=log-depositor MINIO_SECRET_KEY=minioadmin MINIO_ENDPOINT=localhost:9000 MINIO_BUCKET=log-files LOG_FILE_PATH=./log_file.json python log_collection.py
