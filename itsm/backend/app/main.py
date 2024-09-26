from fastapi import FastAPI,Depends
from app.api.v1.user import router as user_router
from app.api.v1.auth import router as auth_router 
from app.middleware.auth_middleware import AuthMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Add custom authentication middleware

origins = [
    "http://192.168.1.8:3000",  # React app URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(AuthMiddleware)

# Public route - anyone can access this
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI User Management System"}

# Include routers
app.include_router(user_router, prefix="/api/v1", dependencies=[Depends(oauth2_scheme)])  # Protected routes
app.include_router(auth_router, prefix="/auth")    # Public + protected auth routes
