import os

from loguru import logger

from boto3.resources.base import ServiceResource

class S3Service(object):

    def __init__(self, client: ServiceResource):
        self._client = client

    def upload(self, file_path: str, folder: str, file_name: str) -> None:
        try:
            self._client.upload_file(file_path, "amsvideo001", f"{folder}/{file_name}")
        except Exception as e: 
            logger.error(e)

