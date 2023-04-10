import random

from pymongo.database import Database
from mimesis.random import Random
from mimesis import Datetime

from app.models.backup import Backup

def insert_backup(db: Database, random_generator: Random) -> Backup: 
    collection = db.backups 
    random_date_generator = Datetime()

    backup = {
        "stream_id": random_generator.randstr(),
        "file_path": random_generator.randstr(),
        "external_filepath": f"s3://{random_generator.randstr()}",
        "created_at": random_date_generator.datetime(2018)                      
    }

    collection.insert_one(backup)

    return backup



def insert_backups(db: Database, random_generator: Random) -> None:
    limit = random.randint(1, 200)

    for _ in range(limit):
        insert_backup(db, random_generator)