from contextlib import asynccontextmanager
from fastapi import UploadFile as File
from aiobotocore.session import get_session

from app.settings.config import settings


class S3Service:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.S3_ACCESS_KEY,
            "aws_secret_access_key": settings.S3_PIVATE_KEY,
            "endpoint_url": settings.S3_URL,
            "verify": False,
        }
        self.bucket_name = settings.S3_BUCKET_NAME
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file: File, object_name: str):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name + "." + settings.S3_FILE_FORMAT,
                    Body=file,
                )
        except Exception as e:
            raise e

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name + "." + settings.S3_FILE_FORMAT,
                )
        except Exception as e:
            raise e


s3_service = S3Service()
