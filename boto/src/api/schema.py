from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class ScrapedDataSchema(BaseModel):
    rk_id: str = Field(max_length=65)
    img_bytes: Optional[bytes] = None
    geo: str = Field(max_length=50)
    domain: str = Field(max_length=50)
    fingerprint: str = Field(max_length=255)
    text_ad: Optional[str] = None
    google_url: Optional[str] = None
    ad_url: Optional[str] = None
    status: str = Field(max_length=20)
