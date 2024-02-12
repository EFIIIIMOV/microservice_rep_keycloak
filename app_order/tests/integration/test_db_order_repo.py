# /tests/integration/app_repositories/test_db_delivery_repo.py

from datetime import datetime
from uuid import UUID, uuid4

import pytest

from app.models.order import Order, OrderStatus
from app.repositories.db_order_repo import OrderRepo


@pytest.fixture()
def order_repo() -> OrderRepo:
    repo = OrderRepo()
    return repo


@pytest.fixture(scope='session')
def order_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_order() -> Order:
    return Order(ord_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), status=OrderStatus.CREATE,
                 address_info='test_address_info_1', customer_info='test_customer_info_1',
                 create_date=datetime.now(), completion_date=datetime.now(),
                 order_info='test_order_info_1')


@pytest.fixture(scope='session')
def second_order() -> Order:
    return Order(ord_id=UUID('14ccc207-9a81-47e6-98ac-53857e32954c'), status=OrderStatus.CREATE,
                 address_info='test_address_info_1', customer_info='test_customer_info_1',
                 create_date=datetime.now(), completion_date=datetime.now(),
                 order_info='test_order_info_1')


# def test_empty_list(order_repo: OrderRepo) -> None:
#     order_repo.delete_all_orders()
#     assert order_repo.get_order() == []


def test_add_first_order(first_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.create_order(first_order) == first_order


def test_add_first_order_repeat(first_order: Order, order_repo: OrderRepo) -> None:
    with pytest.raises(KeyError):
        order_repo.create_order(first_order)


def test_get_order_by_id(first_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.get_order_by_id(first_order.ord_id) == first_order


def test_get_order_by_id_error(order_repo: OrderRepo) -> None:
    with pytest.raises(KeyError):
        order_repo.get_order_by_id(uuid4())


def test_add_second_order(first_order: Order, second_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.create_order(second_order) == second_order
    deliveries = order_repo.get_order()
    assert len(deliveries) == 2
    assert deliveries[0] == first_order
    assert deliveries[1] == second_order


def test_set_status(first_order: Order, order_repo: OrderRepo) -> None:
    first_order.status = OrderStatus.ACCEPTED
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.PICK_UP
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.DELIVERING
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.DELIVERED
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.PAID
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.DONE
    assert order_repo.set_status(first_order).status == first_order.status


def test_delete_created_order(first_order: Order, second_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.delete_order_by_id(first_order.ord_id) == first_order
    assert order_repo.delete_order_by_id(second_order.ord_id) == second_order
