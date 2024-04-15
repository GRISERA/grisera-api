from typing import Optional, Any

from pydantic import BaseModel


class BaseModelOut(BaseModel):
    """
    Base model for models used as a response, with links and errors

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None
