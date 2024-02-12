from uuid import uuid4

import pytest

from app.models.order import OrderStatus
from app.repositories.local_order_repo import OrderRepo
from app.services.order_service import OrderService


@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService(OrderRepo(clear=True))


@pytest.fixture(scope='session')
def first_order_data() -> tuple[str, str, str]:
    return ('test_address_info_1', 'test_customer_info_1', 'test_order_info_1')


@pytest.fixture(scope='session')
def second_order_data() -> tuple[str, str, str]:
    return ('test_address_info_2', 'test_customer_info_2', 'test_order_info_2')


def test_empty_deliveries(order_service: OrderService) -> None:
    assert order_service.get_order() == []


def test_create_first_order(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    address_info, customer_info, order_info = first_order_data
    order = order_service.create_order(address_info, customer_info, order_info)
    assert order.address_info == address_info
    assert order.customer_info == customer_info
    assert order.status == OrderStatus.CREATE
    assert order.completion_date == None
    assert order.order_info == order_info


def test_create_second_order(
        second_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    address_info, customer_info, order_info = second_order_data
    order = order_service.create_order(address_info, customer_info, order_info)
    assert order.address_info == address_info
    assert order.customer_info == customer_info
    assert order.status == OrderStatus.CREATE
    assert order.completion_date == None
    assert order.order_info == order_info


def test_get_order_full(
        first_order_data: tuple[str, str, str],
        second_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    orders = order_service.get_order()
    assert len(orders) == 2
    assert orders[0].address_info == first_order_data[0]
    assert orders[1].address_info == second_order_data[0]


def test_done_order_status_error(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    with pytest.raises(ValueError):
        orders = order_service.get_order()
        order_service.done_order(orders[0].ord_id)


def test_done_order_not_found(
        order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.done_order(uuid4())


def test_accepted_order_not_found(
        order_service: OrderService
) -> None:
    with pytest.raises(KeyError):
        order_service.accepted_order(uuid4())


def test_accepted_order(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    order = order_service.get_order()[0]
    order_service.accepted_order(order.ord_id)
    assert order.status == OrderStatus.ACCEPTED
    assert order.ord_id == order_service.get_order()[0].ord_id


def test_done_order(
        first_order_data: tuple[str, str, str],
        order_service: OrderService
) -> None:
    order = order_service.get_order()[0]
    order.status = OrderStatus.PAID
    order_service.done_order(order.ord_id)
    assert order.status == OrderStatus.DONE
    assert order.ord_id == order_service.get_order()[0].ord_id
