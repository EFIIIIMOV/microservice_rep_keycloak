from typing import Optional
from uuid import UUID

from app.models.order import Order

# orders: list[Order] = [
#     Order(ord_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), status=OrderStatus.CREATE, address_info='test_address_info_0', customer_info='test_customer_info_0',
#           create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), order_info='test_order_info_0'),
#     Order(ord_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), status=OrderStatus.CREATE, address_info='test_address_info_1', customer_info='test_customer_info_1',
#           create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), order_info='test_order_info_1'),
#     Order(ord_id=UUID('45309954-8e3c-4635-8066-b342f634252c'), status=OrderStatus.CREATE, address_info='test_address_info_2', customer_info='test_customer_info_2',
#           create_date=datetime.datetime.now(), completion_date=datetime.datetime.now(), order_info='test_order_info_2'),
# ]

orders = []


class OrderRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            orders.clear()

    def get_order(self) -> list[Order]:
        return orders

    # def get_order_by_id(self, id: UUID) -> Order:
    #     for d in orders:
    #         if d.id == id:
    #             return d
    #
    #     raise KeyError

    def get_order_by_id(self, id: UUID) -> Order:
        for d in orders:
            if d.ord_id == id:
                return d

        raise KeyError

    def create_order(self, order: Order) -> Order:
        if len([d for d in orders if d.ord_id == order.ord_id]) > 0:
            raise KeyError

        orders.append(order)
        return order

    def set_status(self, order: Order) -> Order:
        for d in orders:
            if d.ord_id == order.ord_id:
                d.status = order.status
                break

        return order

    def delete_order(self, id: UUID) -> Optional[Order]:
        for i, order in enumerate(orders):
            if order.ord_id == id:
                deleted_order = orders.pop(i)
                return deleted_order

        return None
