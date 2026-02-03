from fastapi import HTTPException, status
from sqlalchemy import select
import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Initialize S3 client with explicit credentials
s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

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
    
    if not key:
        return None
    
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket_name,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )
        return url
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        print(f"S3 Error: {error_code} - {error_msg}")
        print(f"Bucket: {bucket_name}, Key: {key}, Region: {os.getenv('AWS_REGION')}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate signed URL: {error_code} - {error_msg}"
        )
    except Exception as e:
        print(f"Unexpected error generating signed URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate signed URL: {str(e)}"
        )



