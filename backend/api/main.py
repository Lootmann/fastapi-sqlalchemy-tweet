from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.auths import router as auth_router
from api.routers.likes import router as like_router
from api.routers.tweets import router as tweet_router
from api.routers.users import router as user_router

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(like_router)
app.include_router(tweet_router)
app.include_router(user_router)
