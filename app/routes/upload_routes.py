import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.admin import Admin
from app.routes.admin_routes import get_current_admin
from app.routes.route_utilities import generate_presigned_put_url
from app.schemas.upload_schema import PresignedUploadRequest, PresignedUploadResponse

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def sanitize_filename(file_name: str) -> str:
    # Remove path separators/path traversal and keep only filename.
    base_name = file_name.replace("\\", "/").split("/")[-1].strip()

    # Restrict to safe characters for object keys.
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "-", base_name)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")

    if not cleaned or cleaned in {".", ".."}:
        return "file"
    return cleaned


def build_product_image_key(file_name: str) -> str:
    return f"products/{uuid.uuid4()}-{sanitize_filename(file_name)}"


@router.post("/presigned-url", response_model=PresignedUploadResponse)
def create_presigned_upload_url(
    payload: PresignedUploadRequest,
    _: Admin = Depends(get_current_admin),
):
    if payload.contentType not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid contentType. Allowed types: "
                "image/jpeg, image/png, image/webp, image/gif"
            ),
        )

    key = build_product_image_key(payload.fileName)
    upload_url = generate_presigned_put_url(
        key=key,
        content_type=payload.contentType,
        expires_in=300,
    )

    return {"uploadUrl": upload_url, "key": key}
