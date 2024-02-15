from uuid import UUID
import json
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
from fastapi import Request

order_router = APIRouter(prefix='/order', tags=['Order'])
metrics_router = APIRouter(tags=['Metrics'])

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "order-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'order Service'
tracer = trace.get_tracer(name)

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_order_count = prometheus_client.Counter(
    "get_order_count",
    "Total got all order"
)

created_order_count = prometheus_client.Counter(
    "created_order_count",
    "Total created order"
)

accepted_order_count = prometheus_client.Counter(
    "accepted_order_count",
    "Total accepted order"
)

paid_order_count = prometheus_client.Counter(
    "paid_order_count",
    "Total paid order"
)

done_order_count = prometheus_client.Counter(
    "done_order_count",
    "Total done order"
)

cancelled_order_count = prometheus_client.Counter(
    "cancelled_order_count",
    "Total canceled order"
)


def user_admin(role):
    if role == "service_user" or role == "service_admin":
        return True
    return False


def admin(role):
    if role == "service_admin":
        return True
    return False


@order_router.get('/')
def get_orders(order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> list[Order]:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_order_count.inc(1)
                    return order_service.get_order()
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')


@order_router.post('/add')
async def add_order(request: Request, order_service: OrderService = Depends(OrderService),
                    user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        request_body = await request.body()
        request_data = json.loads(request_body)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    created_order_count.inc(1)
                    order = order_service.create_order(request_data.get("address_info"),
                                                       request_data.get("customer_info"),
                                                       request_data.get("order_info"))
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(400, f'Order with id= already exists')


@order_router.get('/{id}')
def get_order_by_id(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_order_count.inc(1)
                    return order_service.get_order_by_id(id)
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')


@order_router.post('/{id}/accepted')
def accepted_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    accepted_order_count.inc(1)
                    order = order_service.accepted_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/pick_up')
def pick_up_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    order = order_service.pick_up_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/delivering')
def delivering_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    order = order_service.delivering_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/delivered')
def delivered_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    order = order_service.delivered_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/paid')
def paid_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    paid_order_count.inc(1)
                    order = order_service.paid_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/done')
def done_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    done_order_count.inc(1)
                    order = order_service.done_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/cancel')
def cancel_delivery(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    cancelled_order_count.inc(1)
                    order = order_service.cancel_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@order_router.post('/{id}/delete')
def delete_order(id: UUID, order_service: OrderService = Depends(OrderService), user: str = Header(...)) -> Order:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    order = order_service.delete_order(id)
                    return order.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be activated')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
