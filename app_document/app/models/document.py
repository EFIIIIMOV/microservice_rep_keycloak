from datetime import datetime
from uuid import UUID
from uuid import UUID

from pydantic import ConfigDict, BaseModel


#from typing import Optional


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doc_id: UUID
    ord_id: UUID
    type: str
    customer_info: str
    create_date: datetime
    doc: str


class CreateDocumentRequest(BaseModel):
    ord_id: UUID
    type: str
    doc: str
    customer_info: str
