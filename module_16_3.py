from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {"1": "Имя: Example, возраст: 18"}


@app.get("/users")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def user_post(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username"
    , example="SatosiNakomoto")], age: int = Path(ge=18, le=100, description="Enter age", example="25")) -> str:
    next_user_id = str(int(max(users, key=int)) + 1)
    users[next_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {next_user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def user_put(user_id: Annotated[int, Path(description="Enter user ID", example="1")]
                   , username: str = Path(min_length=5, max_length=20, description="Enter username", example="SatosiNakomoto")
                   , age: int = Path(ge=18, le=100, description="Enter age", example="22")) -> str:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
async def user_del(user_id: Annotated[int, Path(description="Enter user ID", example="2")]) -> str:
    key = str(user_id)
    del users[key]
    return f"User {user_id} has been dead"
