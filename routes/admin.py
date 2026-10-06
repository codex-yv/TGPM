from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from utils.package import db_add_packages, db_add_new_category

from database.configs import get_db_depends

from schemas.responses import PackagePostResponse, CategoryPostResponse
from schemas.package import CategorySchema

router = APIRouter(prefix='/api/admin', tags=['Private APIs'])



@router.post('/package', response_model = PackagePostResponse)
async def postTourPackages(images: List[UploadFile] | None = File(None),
                           data: str = Form(...),
                           db: Session = Depends(get_db_depends)):
    result = await db_add_packages(images=images, data = data, db = db)
    return PackagePostResponse(**result)


@router.post('/categories')
async def createCategory(data: CategorySchema, db: Session = Depends(get_db_depends)):
    result = await db_add_new_category(data = data, db = db)
    return CategoryPostResponse(**result)