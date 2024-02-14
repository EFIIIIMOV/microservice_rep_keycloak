from fastapi import FastAPI, Depends, Request, APIRouter
from starlette.middleware.sessions import SessionMiddleware
import httpx
from app.endpoints.auth_router import get_user_role
from app.endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
from uuid import UUID

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
    print(current_user)
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)
    
# @user_router.get("/order/add")
# def add_order(request: Request, current_user: dict = Depends(get_user_role)):
#     print(f"\n/order/add_order\n")
#     if current_user['id'] == '':
#         request.session['prev_url'] = str(request.url)
#         return RedirectResponse(url=auth_url)
#     else:
#         return proxy_request(service_name="order", path="/order/add/", user_info=current_user, request=request)

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


@user_router.post('/order/{id}/accepted')
def accepted_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    print(current_user)
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=auth_url)
    else:
        return proxy_request(service_name="order", path=f"/order/{id}/accepted", user_info=current_user, request=request)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(staff_router)

# from fastapi import FastAPI, Depends, Request, APIRouter
# from starlette.middleware.sessions import SessionMiddleware
# import httpx
# from app.endpoints.auth_router import get_user_role
# from app.endpoints.auth_router import auth_router
# from starlette.responses import RedirectResponse
# from uuid import UUID

# host_ip = "localhost"
# auth_url = "http://localhost:8000/auth/login"

# app = FastAPI(title='Service')

# user_router = APIRouter(prefix='/user', tags=['user'])
# staff_router = APIRouter(prefix='/staff', tags=['staff'])
# app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')

# MICROSERVICES = {
#     "order": "http://localhost:80/api",
# }

# def proxy_request(service_name: str, path: str, request: Request):
#     url = f"{MICROSERVICES[service_name]}{path}"
#     timeout =  20
#     token = request.session.get('auth_token')
#     headers = {
#         'user': str(request.state.user_info),
#         'Authorization': f'Bearer {token}' if token else ''
#     }
#     print(request.method)
#     if request.method == 'GET':
#         response = httpx.get(url, headers=headers, timeout=timeout).json()
#     elif request.method == 'POST':
#         response = httpx.post(url, headers=headers, timeout=timeout).json()
#     elif request.method == 'PUT':
#         response = httpx.put(url, headers=headers).json()
#     elif request.method == 'DELETE':
#         response = httpx.delete(url, headers=headers).json()
#     return response

# @user_router.get("/order")
# def read_order(request: Request, current_user: dict = Depends(get_user_role)):
#     print(current_user)
#     if not current_user['id']:
#         request.session['prev_url'] = str(request.url)
#         return RedirectResponse(url=auth_url)
#     else:
#         request.state.user_info = current_user
#         return proxy_request(service_name="order", path="/order/", request=request)

# @user_router.post('/order/{id}/accepted')
# def accepted_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
#     print(current_user)
#     if not current_user['id']:
#         request.session['prev_url'] = str(request.url)
#         return RedirectResponse(url=auth_url)
#     else:
#         request.state.user_info = current_user
#         return proxy_request(service_name="order", path=f"/order/{id}/accepted", request=request)

# app.include_router(auth_router)
# app.include_router(user_router)
# app.include_router(staff_router)