from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.models import Packages, Categories, Destinations
from database.configs import get_db_depends

from schemas.responses import PackageGetResponse, CategoriesGetResponse, DestinationGetResponse


router = APIRouter(prefix='/api/public', tags=["Public APIs"])

@router.get('/packages', response_model = list[PackageGetResponse])
async def getTourPackages(db: Session = Depends(get_db_depends)):
    data = db.query(Packages).all()

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
    data = db.query(Packages).filter(Packages.id == package_id).scalar()
    return data
