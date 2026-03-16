from fastapi import APIRouter, Query

from app.routes.route_utilities import list_s3_object_keys

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/keys", response_model=list[str])
def get_image_keys(
    prefix: str | None = Query(None, description="Optional prefix to filter keys"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of keys to return"),
):
    """Return a JSON array of S3 object keys for autocomplete.

    The endpoint is intentionally readable without authentication to allow the frontend
    to provide suggestions. If you want to restrict to admin, add a dependency on
    `get_current_admin` from `app.routes.admin_routes`.
    """
    keys = list_s3_object_keys(prefix=prefix, limit=limit)
    return keys
