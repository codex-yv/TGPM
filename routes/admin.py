from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from utils.package import db_add_packages

from database.configs import get_db_depends

from schemas.responses import PackagePostResponse

router = APIRouter(prefix='/api/admin', tags=['Private APIs'])

# List[UploadFile] = File(...)
@router.post('/package', response_model = PackagePostResponse)
async def postTourPackages(images: List[UploadFile] | None = File(None),
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