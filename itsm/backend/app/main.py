from fastapi import FastAPI
from app.api.v1.user import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI User Management System"}
