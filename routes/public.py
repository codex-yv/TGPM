from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database.models import Packages, Categories, Destinations
from database.configs import get_db_depends

from schemas.responses import PackageGetResponse, CategoriesGetResponse, DestinationGetResponse

from utils.package import db_get_package_by_package_id, db_get_all_package, db_filter_packages

import ast

router = APIRouter(prefix='/api/public', tags=["Public APIs"])

@router.get('/packages', response_model = list[PackageGetResponse])
async def getTourPackages(db: Session = Depends(get_db_depends)):
    data = await db_get_all_package(db = db)

    return data


@router.get('/categories', response_model = list[CategoriesGetResponse])
async def getCategories(db: Session = Depends(get_db_depends)):
    data = db.query(Categories).all()
    return data


@router.get('/destinations', response_model = list[DestinationGetResponse])
async def getCategories(db: Session = Depends(get_db_depends)):
    data = db.query(Destinations).all()
    return data

@router.get('/package/{package_id}', response_model = PackageGetResponse | None)
async def getPackageByID(package_id: int, db:Session = Depends(get_db_depends)):
    data = await db_get_package_by_package_id(package_id=package_id, db=db)
    return data


@router.get('/filter', response_model=list[PackageGetResponse])
async def filterPackages(
    destination_id: Optional[int] = Query(None, description="Filter by destination ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    duration: Optional[int] = Query(None, description="Duration in days"),
    availability: Optional[bool] = Query(None, description="Package availability (status)"),
    db: Session = Depends(get_db_depends)
):
    packages = await db_filter_packages(
        db=db,
        destination_id=destination_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        duration=duration,
        availability=availability
    )

    return packages

