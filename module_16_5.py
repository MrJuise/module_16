from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="16_module/templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})


@app.post("/user/{username}/{age}")
async def user_post(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username"
    , example="SatosiNakomoto")], age: int = Path(ge=18, le=100, description="Enter age", example="25")):
    new_id = 1 if not users else users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def user_put(user_id: Annotated[int, Path(description="Enter user ID", example="1")]
                   , username: str = Path(min_length=5, max_length=20, description="Enter username"
            , example="SatosiNakomoto"), age: int = Path(ge=18, le=100, description="Enter age", example="22")):
    for user in users:
        if user_id == user.id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def user_del(user_id: int):
    for index, user in enumerate(users):
        if user_id == user.id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail="User was not found")
