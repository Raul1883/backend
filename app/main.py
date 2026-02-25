from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api import quest_dep

from app.db.db import init_db
from app.config import config

app = FastAPI()

#CORS CONFIG
origins = [
    config.CLIENT_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LIFESPAN CONFIG
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="ttr manager",
    description="api for ttr manager",
    lifespan=lifespan
)

app.include_router(quest_dep.router)

@app.get("/")
def read_root():
    return {"hello": "world"}




