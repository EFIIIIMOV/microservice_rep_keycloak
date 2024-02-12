from fastapi import FastAPI, HTTPException, Depends, Request, Form, APIRouter
from uuid import UUID
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import httpx
from gateway.endpoints.auth_router import get_user_role
from gateway.endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
from enum import Enum
import logging

host_ip = "localhost"
auth_url = "http://localhost:8000/auth/login"

# logging.basicConfig()

app = FastAPI(title='Service')

user_router = APIRouter(prefix='/user', tags=['user'])
staff_router = APIRouter(prefix='/staff', tags=['staff'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
# app.include_router(auth_router)
# app.include_router(user_router)
# app.include_router(staff_router)

MICROSERVICES = {
    "order": "http://localhost:80/api",
}


def proxy_request(service_name: str, path: str, user_info, request: Request):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url, headers=headers).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url, headers=headers).json()
    return response


@user_router.get("/order")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    print("\nread_order\n")
    if current_user['id'] == '':
        print("\nid=''\n")
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(staff_router)
