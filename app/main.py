from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from .config import ConfigClass
from .api_registry import api_registry

app = FastAPI(
    title="Notification Service",
    description="Service for notifications",
    docs_url="/v1/api-doc",
    version=ConfigClass.version
)
app.add_middleware(DBSessionMiddleware, db_url=ConfigClass.SQLALCHEMY_DATABASE_URI)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API registry
## v1
api_registry(app)
