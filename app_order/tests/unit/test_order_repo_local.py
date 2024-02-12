# /tests/unit/test_printing_repo.py

from datetime import datetime
from uuid import uuid4, UUID

import pytest

from app.models.order import Order, OrderStatus
from app.repositories.local_order_repo import OrderRepo

order_test_repo = OrderRepo()


def test_empty_list() -> None:
    assert order_test_repo.get_order() == []


def test_add_first_order() -> None:
    order = Order(ord_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), status=OrderStatus.CREATE,
                  address_info='test_address_info_0', customer_info='test_customer_info_0',
                  create_date=datetime.now(), completion_date=datetime.now(),
                  order_info='test_order_info_0')
    assert order_test_repo.create_order(order) == order


def test_add_first_order_repeat() -> None:
    order = Order(ord_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), status=OrderStatus.CREATE,
                  address_info='test_address_info_0', customer_info='test_customer_info_0',
                  create_date=datetime.now(), completion_date=datetime.now(),
                  order_info='test_order_info_0')
    # order_test_repo.create_order(order)
    with pytest.raises(KeyError):
        order_test_repo.create_order(order)


def test_get_order_by_id() -> None:
    order = Order(ord_id=uuid4(), status=OrderStatus.CREATE,
                  address_info='test_address_info_0', customer_info='test_customer_info_0',
                  create_date=datetime.now(), completion_date=datetime.now(),
                  order_info='test_order_info_0')
    order_test_repo.create_order(order)
    assert order_test_repo.get_order_by_id(order.ord_id) == order


def test_get_order_by_id_error() -> None:
    with pytest.raises(KeyError):
        order_test_repo.get_order_by_id(uuid4())


def test_set_status() -> None:
    order = Order(ord_id=uuid4(), status=OrderStatus.CREATE,
                  address_info='test_address_info_0', customer_info='test_customer_info_0',
                  create_date=datetime.now(), completion_date=datetime.now(),
                  order_info='test_order_info_0')
    order_test_repo.create_order(order)

    order.status = OrderStatus.CREATE
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.PICK_UP
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.DELIVERING
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.DELIVERED
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.PAID
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.DONE
    assert order_test_repo.set_status(order).status == order.status
