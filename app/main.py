from fastapi import FastAPI
from app.routers import challenges

app = FastAPI()
app.include_router(challenges.router)


