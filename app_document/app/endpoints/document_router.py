from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi import Response
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
metrics_router = APIRouter(tags=['Metrics'])

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "document-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'Document Service'
tracer = trace.get_tracer(name)

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_document_count = prometheus_client.Counter(
    "get_document_count",
    "Total got all document"
)

created_document_count = prometheus_client.Counter(
    "created_document_count",
    "Total created document"
)

deleted_document_count = prometheus_client.Counter(
    "deleted_document_count",
    "Total deleted document"
)


def user_admin(role):
    if role == "service_user" or role == "service_admin":
        return True
    return False


def admin(role):
    if role == "service_admin":
        return True
    return False


@document_router.get('/')
def get_document(document_service: DocumentService = Depends(DocumentService), user: str = Header(...)) -> list[
    Document]:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get document"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_document_count.inc(1)
                    return document_service.get_document()
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')


@document_router.get('/{id}')
def get_document_by_id(id: UUID, document_service: DocumentService = Depends(DocumentService),
                       user: str = Header(...)) -> Document:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get document"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_document_count.inc(1)
                    return document_service.get_document_by_id(id)
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')


@document_router.post('/{id}/delete')
def delete_document(id: UUID, document_service: DocumentService = Depends(DocumentService),
                    user: str = Header(...)) -> Document:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Delete document"):
            if user['id'] is not None:
                if admin(user['role']):
                    deleted_document_count.inc(1)
                    document = document_service.delete_document(id)
                    return document.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Document with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Document with id={id} can\'t be deleted')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
