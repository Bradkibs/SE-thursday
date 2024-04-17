from fastapi import FastAPI, status
from auth_endpoints import router


app = FastAPI()
app.include_router(router)

@app.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"message": "This is your first api Hurray!!"}