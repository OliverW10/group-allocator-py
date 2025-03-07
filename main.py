from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import SECRET_KEY, router as auth_router
from api import router as api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Middleware for session management
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(auth_router, prefix="/auth")
app.include_router(api_router, prefix="/api")
# Mount static files last so other routes take precedence
app.mount("/", StaticFiles(directory="static", html=True), name="static")
