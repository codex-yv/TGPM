from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from utils.package import db_add_packages, db_add_new_category, db_add_new_destination, db_toggle_package_status, db_update_package

from database.configs import get_db_depends

from schemas.responses import PackagePostResponse, CategoryPostResponse, DestinationPostResponse, ToggleResponse, PackageUpdationResponse
from schemas.package import CategorySchema, DestinationSchema, PackageToggleSchema, UpadtePackageSchema

router = APIRouter(prefix='/api/admin', tags=['Private APIs'])



@router.post('/package', response_model = PackagePostResponse)
async def postTourPackages(images: List[UploadFile] | None = File(None),
                           data: str = Form(...),
                           db: Session = Depends(get_db_depends)):
    result = await db_add_packages(images=images, data = data, db = db)
    return PackagePostResponse(**result)


@router.post('/categories', response_model = CategoryPostResponse)
async def createCategory(data: CategorySchema, db: Session = Depends(get_db_depends)):
    result = await db_add_new_category(data = data, db = db)
    return CategoryPostResponse(**result)


@router.post('/destinations', response_model=DestinationPostResponse)
async def createCategory(data: DestinationSchema, db: Session = Depends(get_db_depends)):
    result = await db_add_new_destination(data = data, db = db)
    return DestinationPostResponse(**result)

@router.post('/toggle', response_model=ToggleResponse)
async def toggleStatus(package_id:PackageToggleSchema, db: Session = Depends(get_db_depends)):
    result = await db_toggle_package_status(data = package_id.package_id, db = db)
    return ToggleResponse(**result)

@router.post('/update/{package_id}')
async def updatePackage(package_id:int, images: List[UploadFile]| None = File(None), data: str = Form(...), db: Session = Depends(get_db_depends)):
    res = await db_update_package(package_id=package_id, images=images, data=data,  db=db)
    return res