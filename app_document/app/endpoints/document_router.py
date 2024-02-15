from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header

from app.models.document import Document, CreateDocumentRequest
from app.services.document_service import DocumentService
import prometheus_client
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from fastapi import Request

document_router = APIRouter(prefix='/document', tags=['Document'])


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

# @document_router.get('/')
# def get_document(document_service: DocumentService = Depends(DocumentService)) -> list[Document]:
#     return document_service.get_document()

@document_router.get('/')
def get_document(document_service: DocumentService = Depends(DocumentService), user: str = Header(...)) -> list[Document]:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    return document_service.get_document()
                raise HTTPException(403)
    except KeyError:
            raise HTTPException(404, f'Order with id={id} not found')


# @document_router.get('/{id}')
# def get_document_by_id(document_service: DocumentService = Depends(DocumentService)) -> list[Document]:
#     return document_service.get_document()

@document_router.get('/{id}')
def get_document_by_id(id: UUID, document_service: DocumentService = Depends(DocumentService), user: str = Header(...)) -> Document:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_deliveries_count.inc(1)
                    return document_service.get_document_by_id(id)
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')

# @document_router.post('/')
# def add_document(
#         document_info: CreateDocumentRequest,
#         order_service: DocumentService = Depends(DocumentService)
# ) -> Document:
#     try:
#         document = order_service.create_document(document_info.ord_id, document_info.type, document_info.doc,
#                                                  document_info.customer_info)
#         return document.dict()
#     except KeyError:
#         raise HTTPException(400, f'Order with id={document_info.doc_id} already exists')


# @document_router.post('/{id}/delete')
# def delete_document(id: UUID, document_service: DocumentService = Depends(DocumentService)) -> Document:
#     try:
#         document = document_service.delete_document(id)
#         return document.dict()
#     except KeyError:
#         raise HTTPException(404, f'Document with id={id} not found')

@document_router.post('/{id}/delete')
def delete_document(id: UUID, document_service: DocumentService = Depends(DocumentService),user: str = Header(...)) -> Document:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    document = document_service.delete_document(id)
                    return document.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be deleted')
