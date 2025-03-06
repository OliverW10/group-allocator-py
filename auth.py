from fastapi import APIRouter, FastAPI, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse

# Load environment variables
config = Config()
SECRET_KEY = "your-secret-key"  # Change this to a secure random key
CLIENT_ID = "your-microsoft-client-id"
CLIENT_SECRET = "your-microsoft-client-secret"
REDIRECT_URI = "http://localhost:8000/auth/callback"

oauth = OAuth(config)
oauth.register(
    name="microsoft",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    authorize_params={"scope": "openid profile email"},
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    access_token_params=None,
    client_kwargs={"scope": "openid profile email"},
)

router = APIRouter()

@router.get("/api/auth/login")
async def login(request: Request):
    redirect_uri = REDIRECT_URI
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)

@router.get("/api/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.microsoft.authorize_access_token(request)
    user = await oauth.microsoft.parse_id_token(request, token)
    request.session["user"] = user
    return {"message": "Authentication successful", "user": user}

@router.get("/api/auth/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")

@router.get("/api/auth/user")
async def get_user(request: Request):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    return user
