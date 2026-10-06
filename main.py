from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
import json

from database.configs import REDIS, engine, Base, get_db_depends

from utils.package import db_add_packages

from schemas.responses import PackagePostResponse

from routes.public import router as public_router
from routes.admin import router as private_router


app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(public_router)
app.include_router(private_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials= True,
    allow_headers=['*'],
    allow_methods=['*'],
)

@app.get("/health")
def getServerHealth():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            pg = True

    except Exception as e:
        pg = False

    try:
        r = REDIS.ping()
    except Exception as e:
        r = False

    return {
        "server_status": "UP",
        "redis_Status": "UP" if r else "DOWN",
        "pg_status": "UP" if pg else "DOWN"
    }





    
