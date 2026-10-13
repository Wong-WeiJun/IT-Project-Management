import base64
import hashlib
import hmac
import json
from contextvars import ContextVar

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

current_username: ContextVar[str] = ContextVar("current_username", default="System")

ACCOUNTS = {
    "admin": {"password": "admin", "role": "admin"},
    "standard": {"password": "standard", "role": "standard"},
}

PUBLIC_PATHS = {
    "/login",
    "/login.html",
    "/health",
    "/favicon.ico",
}

ADMIN_PAGES = {
    "/audit.html",
}

ADMIN_API_PREFIXES = (
    "/api/audit",
)

SESSION_COOKIE = "escs_session"
SESSION_SECRET = b"glizzy-prototype-secret"

router = APIRouter(tags=["auth"])


def sign_session(data: dict) -> str:
    payload = base64.urlsafe_b64encode(
        json.dumps(data, separators=(",", ":")).encode()
    ).decode()
    signature = hmac.new(SESSION_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def read_session(cookie: str | None) -> dict:
    if not cookie or "." not in cookie:
        return {}
    payload, signature = cookie.rsplit(".", 1)
    expected = hmac.new(SESSION_SECRET, payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return {}
    try:
        data = json.loads(base64.urlsafe_b64decode(payload.encode()))
        return data if isinstance(data, dict) else {}
    except (ValueError, json.JSONDecodeError):
        return {}


def account_for(username: str | None) -> dict | None:
    if not username:
        return None
    account = ACCOUNTS.get(username)
    if not account:
        return None
    return {"username": username, "role": account["role"]}


def user_from_request(request: Request) -> dict | None:
    session = read_session(request.cookies.get(SESSION_COOKIE))
    return account_for(session.get("username"))


def is_admin_request(path: str) -> bool:
    if path in ADMIN_PAGES:
        return True
    return any(path == prefix or path.startswith(prefix + "/") for prefix in ADMIN_API_PREFIXES)


def attach_session(response: Response, username: str, role: str) -> Response:
    response.set_cookie(
        SESSION_COOKIE,
        sign_session({"username": username, "role": role}),
        httponly=True,
        samesite="lax",
    )
    return response


def clear_session(response: Response) -> Response:
    response.delete_cookie(SESSION_COOKIE)
    return response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        user = user_from_request(request)

        if path.startswith("/static") or path in PUBLIC_PATHS:
            if path in ("/login", "/login.html") and request.method == "GET" and user:
                return RedirectResponse("/dashboard.html", status_code=303)
            return await call_next(request)

        if not user:
            if path.startswith("/api/"):
                return JSONResponse({"detail": "Not authenticated"}, status_code=401)
            return RedirectResponse("/login.html", status_code=303)

        token = current_username.set(user["username"])
        try:
            if is_admin_request(path) and user["role"] != "admin":
                if path.startswith("/api/"):
                    return JSONResponse(
                        {"detail": "Admin access required"}, status_code=403
                    )
                return RedirectResponse("/forbidden.html", status_code=303)
            return await call_next(request)
        finally:
            current_username.reset(token)


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    account = ACCOUNTS.get(username)
    if not account or account["password"] != password:
        return RedirectResponse("/login.html?error=1", status_code=303)

    return attach_session(
        RedirectResponse("/dashboard.html", status_code=303),
        username,
        account["role"],
    )


@router.get("/logout")
@router.post("/logout")
def logout():
    return clear_session(RedirectResponse("/login.html", status_code=303))


@router.get("/api/auth/me")
def current_user(request: Request):
    user = user_from_request(request)
    if not user:
        return JSONResponse({"detail": "Not authenticated"}, status_code=401)
    return user
