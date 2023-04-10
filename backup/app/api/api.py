from uuid import UUID
import boto3
import os

from pymongo.mongo_client import MongoClient

from app.api.watcher import Watcher
from app.api.producer import Producer
from app.api.supervisor import Supervisor
from app.db.repositories.backup_repository import BackupRepository
from app.aws.services.s3_service import S3Service



def initialize() -> None:
    path = os.environ.get("ACTOR_WATCH_DIR")
    print(path)

    subpaths = os.listdir(path)
    producers = []


    for subpath in subpaths:
        real_path = f"{path}/{subpath}"
        repo = init_mongo()
        s3 = init_s3()
        watcher = init_watcher(real_path, repo, s3)
        producer = Producer(watcher)
        producers.append(producer)
    
    supervisor = Supervisor(producers)
    supervisor.start_processes()
        



def init_mongo() -> BackupRepository:
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")

    db_url = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}"

    client = MongoClient(db_url, uuidRepresentation="standard")
    database = client[db_name]
    coll = database["backups"]

    return BackupRepository(coll)

def init_s3() -> S3Service:
    key_id = os.environ.get("S3_KEY_ID")
    key = os.environ.get("S3_SECRET_KEY")

    s3 = boto3.client(
        service_name="s3",
        region_name="us-east-2",
        aws_access_key_id=key_id,
        aws_secret_access_key=key
    )
    s3_service = S3Service(s3)

    return s3_service

def init_watcher(path: str, repo: BackupRepository, s3: S3Service) -> Watcher:
    actor_wait_time = float(os.environ.get("ACTOR_WAIT_TIME"))
    watcher = Watcher(path, repo, s3, actor_wait_time)

    return watcher