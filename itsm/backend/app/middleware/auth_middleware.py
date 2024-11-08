import logging
from fastapi import Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.db.session import get_db
from app.controller.user_controller import get_user_data
from app.controller.customeruser_controller import get_customeruser_data
from starlette.responses import JSONResponse

# Public routes
PUBLIC_ROUTES = ["/", "/auth/customer/login", "/auth/token", "/public-resource", "/docs", "/openapi.json"]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Secret and Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

def create_error_response(status_code: int, detail: str):
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            logger.error("Authorization header missing")
            return create_error_response(401, "Authorization header missing")

        if not authorization.startswith("Bearer "):
            logger.error("Invalid Authorization header format")
            return create_error_response(401, "Invalid Authorization header format")

        token = authorization.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            usertype = payload.get("usertype") or "agent"

            if not username or not usertype:
                logger.error("Token does not contain a valid username or usertype")
                return create_error_response(401, "Invalid token")

            db: Session = next(get_db())
            if usertype == "agent":
                user = get_user_data(db, username)
            elif usertype == "customeruser":
                user = get_customeruser_data(db, username)
            else:
                logger.error(f"Unknown usertype: {usertype}")
                return create_error_response(401, "Invalid usertype in token")

            if not user:
                logger.error(f"User {username} not found in database")
                return create_error_response(401, "User not found")

            request.state.user = user

        except JWTError as jwt_error:
            logger.error(f"JWT Error: {jwt_error}")
            return create_error_response(401, "Invalid token or token expired")
        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            return create_error_response(500, "Internal server error during authentication")

        response = await call_next(request)
        return response