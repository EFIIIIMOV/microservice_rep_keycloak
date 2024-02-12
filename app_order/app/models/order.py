import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, BaseModel


class OrderStatus(enum.Enum):
    CREATE = 'create'
    ACCEPTED = 'accepted'
    PICK_UP = 'pick_up'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    PAID = 'paid'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # ord_id: UUID
    ord_id: UUID
    status: OrderStatus
    address_info: str
    customer_info: str
    create_date: datetime
    completion_date: Optional[datetime] = None
    order_info: str


class CreateOrderRequest(BaseModel):
    address_info: str
    customer_info: str
    order_info: str
