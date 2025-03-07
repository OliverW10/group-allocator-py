import datetime
import uuid
from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse

# Load environment variables
config = Config()
SECRET_KEY = "your-secret-key" # Change this to a secure random key
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

@router.get("/status")
async def status(request: Request):
    return {"status": "yeah yeah"}

@router.get("/fake-login")
async def fake_login(request: Request, email: str):
    name_part = email.split('@')[0]
    display_name = ' '.join(word.capitalize() for word in name_part.split('.'))
    unique_id = str(uuid.uuid4())
    now = datetime.datetime.now(tz=datetime.UTC)
    token_data = {
            "oid": unique_id,  # Microsoft's object ID
            "sub": unique_id,  # Subject identifier
            "tid": "fake-tenant-id-12345",  # Tenant ID
            "upn": email,  # User Principal Name
            "preferred_username": email,
            "name": display_name,
            "email": email,
            "given_name": display_name.split()[0] if ' ' in display_name else display_name,
            "family_name": display_name.split()[-1] if ' ' in display_name else "",
            "aud": "fake-client-id-12345",  # Audience (your app's client ID)
            "iss": "https://login.microsoftonline.com/fake-tenant-id/v2.0",  # Issuer
            "iat": int(now.timestamp()),  # Issued At
            "exp": int((now + datetime.timedelta(hours=1)).timestamp()),  # Expiration
            "nbf": int(now.timestamp()),  # Not Before
            "roles": ["User"]  # Default role
        }
        
    # Store token data in session, similar to what oauth.microsoft would do
    request.session["user"] = token_data
    
    # Check if email starts with 'marc' for admin access
    if email.lower().startswith('marc'):
        return RedirectResponse(url="/admin.html")
    return RedirectResponse(url="/form.html")

@router.get("/login")
async def login(request: Request):
    redirect_uri = REDIRECT_URI
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.microsoft.authorize_access_token(request)
    user = await oauth.microsoft.parse_id_token(request, token)
    request.session["user"] = user
    return RedirectResponse(url="/form.html")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")

@router.get("/user")
async def get_user(request: Request):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    return user
