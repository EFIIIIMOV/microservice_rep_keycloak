from uuid import UUID

from app.models.order import Order, CreateOrderRequest
from app.services.order_service import OrderService
from fastapi import APIRouter, Depends, HTTPException

order_router = APIRouter(prefix='/order', tags=['Order'])


@order_router.get('/')
def get_order(order_service: OrderService = Depends(OrderService)) -> list[Order]:
    print('\n///get_order///\n')
    return order_service.get_order()


# @order_router.post('/')
# def add_order(
#         order_info: CreateOrderRequest,
#         order_service: OrderService = Depends(OrderService)
# ) -> Order:
#     try:
#         print('\n///post_order///\n')
#         order = order_service.create_order(order_info.ord_id, order_info.address_info, order_info.customer_info,
#                                            order_info.create_date, order_info.completion_date, order_info.order_info)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(400, f'Order with id={order_info.order_id} already exists')

@order_router.post('/')
def add_order(
        order_info: CreateOrderRequest,
        order_service: OrderService = Depends(OrderService)
) -> Order:
    try:
        print('\n///post_order///\n')
        order = order_service.create_order(order_info.address_info, order_info.customer_info,
                                           order_info.order_info)
        return order.dict()
    except KeyError:
        raise HTTPException(400, f'Order with id={order_info.order_id} already exists')


@order_router.post('/{id}/accepted')
def accepted_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.accepted_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/pick_up')
def pick_up_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.pick_up_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be pick_up')


@order_router.post('/{id}/delivering')
def delivering_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.delivering_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be delivering')


@order_router.post('/{id}/delivered')
def delivered_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.delivered_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be delivered')


@order_router.post('/{id}/paid')
def paid_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.paid_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be paid')


@order_router.post('/{id}/done')
def done_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.done_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be done')


@order_router.post('/{id}/cancel')
def cancel_delivery(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.cancel_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be canceled')


@order_router.post('/{id}/delete')
def delete_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.delete_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
