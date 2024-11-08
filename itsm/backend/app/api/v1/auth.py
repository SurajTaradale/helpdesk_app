import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils import hash_password
from app.db.session import get_db
from app.controller.user_controller import get_user_data, get_user_hash_pwd
from app.controller.customeruser_controller import get_customeruser_data, get_customeruser_hash_pwd
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Secret and Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Router for authentication-related routes
router = APIRouter()

# Models
class Token(BaseModel):
    access_token: str
    token_type: str
    user_type :str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    valid_id: int or None = None

class UserInDB(User):
    hashed_password: str

# Utility functions for hashing and token management
def verify_password(plain_password, hashed_password):
    try:
        return plain_password == hashed_password
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password verification failed")

def get_password_hash(password):
    try:
        return hash_password(password)
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error hashing password")

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token creation failed")

# Dependency: Get user from DB by login
def get_user(db: Session, login: str):
    try:
        return get_user_data(db, login)
    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user data")

# Authenticate user
def authenticate_user(db: Session, login: str, password: str):
    try:
        user = get_user(db, login)
        hashed_password = get_user_hash_pwd(db, login)
        password = hash_password(password)
        if not user or not verify_password(password, hashed_password):
            return None
        return user
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication failed")

# Dependency: Get current user based on the token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Token decoding failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token decoding failed")
    
    user = get_user(db, login=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Dependency: Get current active user
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    try:
        if current_user["valid_id"] != 1:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    except AttributeError as e:
        logger.error(f"User object has no attribute 'valid_id': {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid user object")

# Route: Token generation for login
@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    print(user)
    if not user:
        print(user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user['login'],"user_type":"agent"}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer","user_type":"agent"}
    

# Protected route: User details (example route)
@router.get("/me/")
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    try:
        return current_user
    except Exception as e:
        logger.error(f"Failed to fetch current user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user details")

# Dependency: Get user from DB by login
def get_customeruser(db: Session, login: str):
    try:
        return get_customeruser_data(db, login)
    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user data")
    
def authenticate_customeruser(db: Session, login: str, password: str):
    try:
        user = get_customeruser(db, login)
        hashed_password = get_customeruser_hash_pwd(db, login)
        password = hash_password(password)
        if not user or not verify_password(password, hashed_password):
            return None
        return user
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication failed")

# Route: Token generation for login
@router.post("/customer/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_customeruser(db, form_data.username, form_data.password)
    print(user)
    if not user:
        print(user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user['login'],"user_type":"customer"}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user_type":"customer"}