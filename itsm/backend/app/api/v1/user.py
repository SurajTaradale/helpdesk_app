from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controller.user_controller import user_add, get_user_data
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.controller.user_controller import EmailAlreadyExistsError, LoginAlreadyExistsError

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db), change_user_id: int = 1):
    try:
        user_id = user_add(db, user, change_user_id)
        return {"user_id": user_id}
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LoginAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred"+str(e))

@router.get("/user/")
async def get_user(id: int = None, login: str = None, db: Session = Depends(get_db)):
    if id is None and login is None:
        raise HTTPException(status_code=400, detail="Either 'id' or 'login' must be provided")
    
    try:
        if id:
            user = get_user_data(db, id)
        else:
            user = get_user_data(db, login)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
