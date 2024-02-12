# uvicorn app.main:app --reload

import asyncio

from app import rabbitmq
from app.endpoints.order_router import order_router
from fastapi import FastAPI

#from app.endpoints.document_router import document_router
#from app.endpoints.document_router import document_router

app = FastAPI(title='Service')

app.include_router(order_router, prefix='/api')
#app.include_router(document_router, prefix='/api')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))
