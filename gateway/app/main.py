from fastapi import FastAPI, Depends, Request, APIRouter
from starlette.middleware.sessions import SessionMiddleware
import httpx
from gateway.app.endpoints.auth_router import get_user_role
from gateway.app.endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
from uuid import UUID
from app_order.app.models.order import CreateOrderRequest

host_ip = "localhost"
auth_url = "http://localhost:8000/auth/login"

# logging.basicConfig()

app = FastAPI(title='Service')

user_router = APIRouter(prefix='/user', tags=['user'])
staff_router = APIRouter(prefix='/staff', tags=['staff'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')

MICROSERVICES = {
    "order": "http://localhost:80/api",
    "document": "http://localhost:81/api",
}


def proxy_request(service_name: str, path: str, user_info, request: Request, json_data: dict = None):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers, json=json_data, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url, headers=headers, json=json_data).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url, headers=headers).json()
    
    return response

#___ORDER___

@staff_router.get("/order")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        print(f"\nrequest.session['prev_url'] = {request.session['prev_url']}\n")
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)

@user_router.post("/order/add", response_model=CreateOrderRequest)
def add_order(request: Request, order_request: CreateOrderRequest, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/add", user_info=current_user, request=request, json_data=order_request.dict())

@staff_router.post("/order/add", response_model=CreateOrderRequest)
def add_order(request: Request, order_request: CreateOrderRequest, current_user: dict = Depends(get_user_role)):
    print(f"\n/order/add\n")
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/add", user_info=current_user, request=request, json_data=order_request.dict())

@user_router.get("/order/{id}")
def read_order_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}", user_info=current_user, request=request)

@staff_router.get("/order/{id}")
def read_order_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}", user_info=current_user, request=request)

@staff_router.post('/order/{id}/accepted')
def accepted_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/accepted", user_info=current_user, request=request)

@staff_router.post('/order/{id}/pick_up')
def pick_up_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/pick_up", user_info=current_user, request=request)

@staff_router.post('/order/{id}/delivering')
def delivering_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/delivering", user_info=current_user, request=request)

@staff_router.post('/order/{id}/delivered')
def delivered_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/delivered", user_info=current_user, request=request)

@staff_router.post('/order/{id}/paid')
def paid_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/paid", user_info=current_user, request=request)

@staff_router.post('/order/{id}/done')
def done_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/done", user_info=current_user, request=request)

@staff_router.post('/order/{id}/cancel')
def cancel_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/cancel", user_info=current_user, request=request)

@staff_router.post('/order/{id}/delete')
def delete_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/delete", user_info=current_user, request=request)

#___DOCUMENT___

@staff_router.get("/document")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path="/document/", user_info=current_user, request=request)

@staff_router.get("/document/{id}")
def read_order_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path=f"/document/{id}", user_info=current_user, request=request)

@user_router.get("/document/{id}")
def read_order_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path=f"/document/{id}", user_info=current_user, request=request)

@staff_router.post('/document/{id}/delete')
def delete_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="document", path=f"/document/{id}/delete", user_info=current_user, request=request)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(staff_router)