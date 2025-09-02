from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ImportableModel(BaseModel):
    """
    Base model for entities that can be imported from external sources
    
    Attributes:
        external_id (Optional[str]): External ID from import source (e.g. @id from JSON)
    """
    external_id: Optional[str] = None
    import_job_id: Optional[str] = None
    import_timestamp: Optional[datetime] = None

