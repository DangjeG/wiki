from fastapi import FastAPI

from wiki.auth.schemas.user import User

app = FastAPI(
    title="wiki"
)

@app.get("/start")
def start():
    return "hello"

@app.get("/account/{user_id}")
def get_user(user_id: int):
    return user_id

@app.post("/auth")
def enter_emile(user: User):
    return {"status": 200, "email": user.email}
