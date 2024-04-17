from fastapi import FastAPI, status
from auth_endpoints import auth_router
from inventory_management_endpoints import item_router



app = FastAPI()
app.include_router(auth_router)
app.include_router(item_router)


@app.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"message": "This is your first api Hurray!!"}