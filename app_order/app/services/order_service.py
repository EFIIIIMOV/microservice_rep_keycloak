# 1. Поменять int на UUID в функциях

import asyncio
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends

from app.models.order import Order, OrderStatus
from app.repositories.db_order_repo import OrderRepo


class OrderService():
    order_repo: OrderRepo

    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo)) -> None:
        self.order_repo = order_repo

    def get_order(self) -> list[Order]:
        print(f"\n////{self.order_repo}////\n")
        return self.order_repo.get_order()

    def create_order(self, address_info: str, customer_info: str, order_info: str) -> Order:
        order = Order(ord_id=uuid4(), status=OrderStatus.CREATE, address_info=address_info, customer_info=customer_info,
                      create_date=datetime.now(), completion_date=None, order_info=order_info)
        return self.order_repo.create_order(order)

    def accepted_order(self, id: UUID) -> Order:
        from app.rabbitmq import send_to_document_queue
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.CREATE:
            raise ValueError

        order.status = OrderStatus.ACCEPTED

        document_data = {
            "doc_id": uuid4(),
            "ord_id": id,
            "type": "Test Type",
            "create_date": datetime.now(),
            "doc": "Test Document",
            "customer_info": order.customer_info
        }

        asyncio.run(send_to_document_queue(document_data))

        return self.order_repo.set_status(order)

    def pick_up_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.ACCEPTED:
            raise ValueError

        order.status = OrderStatus.PICK_UP
        return self.order_repo.set_status(order)

    def delivering_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PICK_UP:
            raise ValueError

        order.status = OrderStatus.DELIVERING
        return self.order_repo.set_status(order)

    def delivered_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.DELIVERING:
            raise ValueError

        order.status = OrderStatus.DELIVERED
        return self.order_repo.set_status(order)

    def paid_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.DELIVERED or OrderStatus.DELIVERING):
            raise ValueError

        order.status = OrderStatus.PAID
        return self.order_repo.set_status(order)

    def done_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PAID:
            raise ValueError

        order.status = OrderStatus.DONE
        order.completion_date = datetime.now()
        return self.order_repo.set_status(order)

    def cancel_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.CREATE or OrderStatus.ACCEPTED):
            raise ValueError

        order.status = OrderStatus.CANCELLED
        return self.order_repo.set_status(order)

    # def delete_order(self, id: UUID) -> None:
    #     order = self.order_repo.get_order_by_id(id)
    #     if not order:
    #         raise ValueError(f'Order with id={id} not found')
    #
    #     return self.order_repo.delete_order(id)
