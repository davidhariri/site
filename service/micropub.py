"""
Micropub service functions. These functions are used to handle Micropub requests.
"""

from typing import IO
from flask import Request
from pydantic_settings import BaseSettings
import boto3

def verify_access_token(request: Request, settings: BaseSettings) -> bool:
    """
    Verify the access token in the Authorization header.
    """
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]

    return token == settings.MICROPUB_SECRET


def upload_file_to_s3(
    file: IO, bucket_name: str, file_key: str, settings: BaseSettings
) -> None:
    """
    Upload a file to an S3 bucket. May raise an exception for various reasons.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    s3.upload_fileobj(
        file, bucket_name, file_key, ExtraArgs={"ContentType": file.content_type}
    )
