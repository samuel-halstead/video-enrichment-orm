from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Timestamps(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[str] = None
