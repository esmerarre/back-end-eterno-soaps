from fastapi import HTTPException, status
from sqlalchemy import select
import boto3
import os
from botocore.exceptions import ClientError

def validate_model(session, cls, model_id):
    try:
        model_id = int(model_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")

    query = select(cls).where(cls.id == model_id)
    model = session.execute(query).scalars().first()

    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__} {model_id} not found")
    return model

# Initialize S3 client
s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))

def generate_signed_url(key: str, expires_in: int = 3600) -> str:
    """Generate a signed URL for an S3 object.
    
    Args:
        key: The S3 object key
        expires_in: URL expiration time in seconds (default: 1 hour)
    
    Returns:
        Signed URL string
    
    Raises:
        HTTPException: If URL generation fails
    """
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    
    if not bucket_name:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AWS_BUCKET_NAME environment variable not set"
        )
    
    try:
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket_name,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate signed URL: {str(e)}"
        )



