from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controller.customeruser_controller import customeruser_add,get_customeruser_data,get_customeruser_search, customer_user_update
from app.db.session import get_db
from app.schemas.customeruserSchema import CustomerUserSchema
from app.controller.customeruser_controller import EmailAlreadyExistsError, LoginAlreadyExistsError, CommanErrorException
from typing import List, Optional
router = APIRouter()

@router.post("/customeruser/")
def create_user(user: CustomerUserSchema, db: Session = Depends(get_db), change_user_id: int = 1):
    try:
        new_user = customeruser_add(db, user, change_user_id)  # Expecting User instance here
        return {"user": new_user} 
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LoginAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred"+str(e))

@router.get("/customeruser/")
async def get_user(id: int = None, login: str = None, db: Session = Depends(get_db)):
    if id is None and login is None:
        raise HTTPException(status_code=400, detail="Either 'id' or 'login' must be provided")
    print(f"userlist {login}")
    try:
        if id:
            user = get_customeruser_data(db, id)
        else:
            user = get_customeruser_data(db, login)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except CommanErrorException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
# @router.get("/userslist/")
# async def get_users_paginated(page_no: int = 1, count_per_page: int = 10, db: Session = Depends(get_db)):
#     """
#     Get a paginated list of users.

#     - **page_no**: The page number to retrieve (default is 1).
#     - **count_per_page**: The number of users per page (default is 10).
#     """
#     try:
#         paginated_users = get_user_list(db, page_no, count_per_page)
#         return paginated_users
#     except CommanErrorException as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.get("/customeruserssearch/")
async def search_users(Search: Optional[str] = None, 
                       UserLogin: Optional[str] = None, 
                       db: Session = Depends(get_db)):
    """
    Search for users based on Search (first_name, last_name, or login), UserLogin (exact match), or PostMasterSearch.
    
    - **Search**: Wildcard search for first name, last name, or login.
    - **UserLogin**: Exact or partial match for the user login.
    """
    try:
        # Call the get_user_search function to handle the search logic
        user_search_results = get_customeruser_search(db, Search, UserLogin)
        return user_search_results
    except CommanErrorException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while searching for users.")
    
@router.put("/customeruser/{user_id}/")
def update_user(user_id: int, user: CustomerUserSchema, db: Session = Depends(get_db), change_user_id: int = 1):
    try:
        updated_user = customer_user_update(db, user_id, user, change_user_id)  # Expecting UserUpdate instance here
        
        return {"user": updated_user}
    except CommanErrorException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LoginAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))