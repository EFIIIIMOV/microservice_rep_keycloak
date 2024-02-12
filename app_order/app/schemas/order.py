from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.models.order import OrderStatus
from app.schemas.base_schema import Base


class Order(Base):
    __tablename__ = 'order'

    ord_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False)
    address_info = Column(String, nullable=False)
    customer_info = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    completion_date = Column(DateTime)
    order_info = Column(String, nullable=False)
