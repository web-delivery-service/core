from contextlib import asynccontextmanager
from fastapi import UploadFile as File
from aiobotocore.session import get_session

from app.settings.config import auth_settings


class S3Client:
    def __init__(self):
        self.config = {
            "aws_access_key_id": auth_settings.S3_ACCESS_KEY,
            "aws_secret_access_key": auth_settings.S3_PIVATE_KEY,
            "endpoint_url": auth_settings.S3_URL,
            "verify": False,
        }
        self.bucket_name = auth_settings.S3_BUCKET_NAME
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
                    Key=object_name + "." + auth_settings.S3_FILE_FORMAT,
                    Body=file,
                )
        except Exception as e:
            raise e

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name + "." + auth_settings.S3_FILE_FORMAT,
                )
        except Exception as e:
            raise e

    async def upload_file_to_group(self, file: File, object_name: str):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=auth_settings.S3_BUCKET_NAME_GROUPS,
                    Key=object_name + "." + auth_settings.S3_FILE_FORMAT,
                    Body=file,
                )
        except Exception as e:
            raise e

    async def delete_file_from_group(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=auth_settings.S3_BUCKET_NAME_GROUPS,
                    Key=object_name + "." + auth_settings.S3_FILE_FORMAT,
                )
        except Exception as e:
            raise e


s3_client = S3Client()
