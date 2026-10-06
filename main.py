from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
import json

from database.configs import REDIS, engine, Base, get_db_depends
from database.models import Packages

from utils.package import db_add_packages

from schemas.package import PackageSchema
from schemas.responses import PackagePostResponse, PackageGetResponse

app = FastAPI()
Base.metadata.create_all(engine)

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


@app.get('/packages', response_model = list[PackageGetResponse])
async def getTourPackages(db: Session = Depends(get_db_depends)):
    data = db.query(Packages).all()
    print(data)

    return data

# List[UploadFile] = File(...)
@app.post('/package', response_model = PackagePostResponse)
async def postTourPackages(images: UploadFile | None = File(None),
                           data: str = Form(...),
                           db: Session = Depends(get_db_depends)):
    # image_id = []
    # for image in images:
    #     image_byte = await image.read()

    #     image_model = PackageImages(
    #         image_bin = image_byte
    #     )

    #     db.add(image_model)
    #     image_id.append(image_model.id)
    result = await db_add_packages(images=images, data = data, db = db)
    return PackagePostResponse(**result)
    




    
