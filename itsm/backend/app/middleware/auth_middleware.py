import logging
from fastapi import Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.db.session import get_db
from app.controller.user_controller import get_user_data
from app.controller.customeruser_controller import get_customeruser_data

# Public routes
PUBLIC_ROUTES = ["/", "/auth/customer/login", "/auth/token", "/public-resource", "/docs", "/openapi.json"]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Secret and Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware for public routes
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            logger.error("Authorization header missing")
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})

        if not authorization.startswith("Bearer "):
            logger.error("Invalid Authorization header format")
            return JSONResponse(status_code=401, content={"detail": "Invalid Authorization header format"})

        token = authorization.split(" ")[1]  # "Bearer <token>"

        try:
            # Decode JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            usertype = payload.get("usertype") or "agent"  # Either 'agent' or 'customeruser'

            if not username or not usertype:
                logger.error("Token does not contain a valid username or usertype")
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            # Check if user exists in the database based on usertype
            db: Session = next(get_db())
            if usertype == "agent":
                user = get_user_data(db, username)
            elif usertype == "customeruser":
                user = get_customeruser_data(db, username)
            else:
                logger.error(f"Unknown usertype: {usertype}")
                return JSONResponse(status_code=401, content={"detail": "Invalid usertype in token"})

            if not user:
                logger.error(f"User {username} not found in database")
                return JSONResponse(status_code=401, content={"detail": "User not found"})

            # Attach the authenticated user to the request state
            request.state.user = user

        except JWTError as jwt_error:
            logger.error(f"JWT Error: {jwt_error}")
            return JSONResponse(status_code=401, content={"detail": "Invalid token or token expired"})

        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error during authentication"})

        # Proceed with the request
        response = await call_next(request)
        return response
