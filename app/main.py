from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import applications, system_schemas, user

from app.api.sessions import genre
from app.api.sessions import system
from app.api.sessions import sessions
from app.api.sessions import company
from app.api import auth
from app.api import characters
from app.api import wiki


from app.db.db import init_db
from app.db.couchdb import couch_client
from app.config import config
from app.exceptions.service_exceptions import AppException
from fastapi.responses import Response


# LIFESPAN CONFIG
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    couch_client.start()
    yield
    await couch_client.stop()


app = FastAPI(title="ttr manager", description="api for ttr manager", lifespan=lifespan)

# CORS CONFIG
origins = [config.CLIENT_URL, "http://localhost:4173", "http://localhost:5173"]
print("origins", origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app_router = APIRouter(
    prefix="/api/v1",
)


@app.options("/{path:path}")
async def handle_options(path: str):
    return Response(status_code=204)


app_router.include_router(user.router)
app_router.include_router(genre.router)
app_router.include_router(system.router)
app_router.include_router(sessions.router)
app_router.include_router(company.router)
app_router.include_router(auth.router)
app_router.include_router(characters.router)
app_router.include_router(applications.router)
app_router.include_router(system_schemas.router)
app_router.include_router(wiki.router)


app.include_router(app_router)


@app.exception_handler(AppException)
async def service_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_type": exc.__class__.__name__},
    )


print(app.routes)


@app.get("/api/v1/")
def read_root():
    return {"Witcher": "sdfssdxcvsd"}
