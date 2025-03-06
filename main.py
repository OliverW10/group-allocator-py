

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api import add_crud_api
from auth import SECRET_KEY, add_auth_controller


app = FastAPI()
# Middleware for session management
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
add_auth_controller(app)
add_crud_api(app)