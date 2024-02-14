from uuid import UUID

from app.models.order import Order, CreateOrderRequest
from app.services.order_service import OrderService
from fastapi import APIRouter, Depends, HTTPException, Response
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header
import prometheus_client
import asyncio
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

order_router = APIRouter(prefix='/order', tags=['Order'])


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "delivery-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Delivery Service'
tracer = trace.get_tracer(name)


delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_deliveries_count = prometheus_client.Counter(
    "get_deliveries_count",
    "Total got all deliveries"
)

created_delivery_count = prometheus_client.Counter(
    "created_delivery_count",
    "Total created deliveries"
)

started_delivery_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started deliveries"
)

completed_delivery_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed deliveries"
)

cancelled_delivery_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled deliveries"
)

def user_admin(role):
    if role == "service_user" or role == "service_admin":
        return True
    return False

def admin(role):
    if role == "service_admin":
        return True
    return False

# @order_router.get('/')
# def get_order(order_service: OrderService = Depends(OrderService)) -> list[Order]:
#     print('\n///get_order///\n')
#     return order_service.get_order()


@order_router.get('/')
def get_deliveries(order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> list[Order]:
    user = eval(user)
    with tracer.start_as_current_span("Get deliveries"):
        if user['id'] is not None:
            if user_admin(user['role']):
                get_deliveries_count.inc(1)
                return order_service.get_order()
            raise HTTPException(403)


# @order_router.post('/')
# def add_order(
#         order_info: CreateOrderRequest,
#         order_service: OrderService = Depends(OrderService)
# ) -> Order:
#     try:
#         print('\n///post_order///\n')
#         order = order_service.create_order(order_info.address_info, order_info.customer_info,
#                                            order_info.order_info)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(400, f'Order with id={order_info.order_id} already exists')
        


@order_router.post('/add')
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


# @order_router.post('/{id}/pick_up')
# def pick_up_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.pick_up_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be pick_up')


# @order_router.post('/{id}/delivering')
# def delivering_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.delivering_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be delivering')


# @order_router.post('/{id}/delivered')
# def delivered_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.delivered_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be delivered')


# @order_router.post('/{id}/paid')
# def paid_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.paid_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be paid')


# @order_router.post('/{id}/done')
# def done_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.done_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be done')


# @order_router.post('/{id}/cancel')
# def cancel_delivery(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.cancel_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
#     except ValueError:
#         raise HTTPException(400, f'Order with id={id} can\'t be canceled')


# @order_router.post('/{id}/delete')
# def delete_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
#     try:
#         order = order_service.delete_order(id)
#         return order.dict()
#     except KeyError:
#         raise HTTPException(404, f'Order with id={id} not found')
