from pydantic import BaseModel, Field


class PresignedUploadRequest(BaseModel):
    fileName: str = Field(min_length=1)
    contentType: str = Field(min_length=1)


class PresignedUploadResponse(BaseModel):
    uploadUrl: str
    key: str
