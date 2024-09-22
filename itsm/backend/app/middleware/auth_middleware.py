import logging
from fastapi import Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.db.session import get_db
from app.controller.user_controller import get_user_data
PUBLIC_ROUTES = ["/", "/auth/token", "/public-resource", "/docs", "/openapi.json"]

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Secret and Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                logger.error("Token does not contain a valid username")
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            # Check if the user exists in the database
            try:
                db: Session = next(get_db())
                user = get_user_data(db, username)
                if not user:
                    logger.error(f"User {username} not found in database")
                    return JSONResponse(status_code=401, content={"detail": "User not found"})
            except Exception as db_error:
                logger.error(f"Database error: {db_error}")
                return JSONResponse(status_code=500, content={"detail": "Internal server error during database lookup"})

            # Attach the authenticated user to the request state
            request.state.user = user

        except JWTError as jwt_error:
            logger.error(f"JWT Error: {jwt_error}")
            return JSONResponse(status_code=401, content={"detail": "Invalid token or token expired"})

        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error during authentication"})

        response = await call_next(request)
        return response
