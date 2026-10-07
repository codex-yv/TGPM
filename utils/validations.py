from sqlalchemy import Select
from sqlalchemy.orm import Session
from database.models import Categories, Destinations, PackageImages

async def db_validate_categories_id(cat_ids:list[int], db:Session) -> dict:
    valid = True
    for cat_id in cat_ids:
        stmt = Select(Categories.id).where(Categories.id == cat_id)
        res = db.execute(stmt).first()
        if not res:
            valid = False
            break

    if valid:
        return {
            "status": valid,
            "message": "All category ids are valid."
        }
    return {
        "status": valid,
        "message": f"{cat_id} is not a valid category id."
    }

async def db_validate_destinations_id(des_ids: list[int], db: Session):
    valid = True
    for des_id in des_ids:
        stmt = Select(Destinations.id).where(Destinations.id == des_id)
        res = db.execute(stmt).first()
        if not res:
            valid = False
            break

    if valid:
        return {
            "status": valid,
            "message": "All Destination ids are valid."
        }
    return {
        "status": valid,
        "message": f"{des_id} is not a valid Destionation id."
    }

async def db_validate_image_id(img_ids: list[int], db: Session):
    valid = True

    for img_id in img_ids:
        stmt = Select(PackageImages.id).where(PackageImages.id == img_id)
        res = db.execute(stmt).first()
        if not res:
            valid = False
            break

    if valid:
        return {
            "status": valid,
            "message": "All Destination ids are valid."
        }
    return {
        "status": valid,
        "message": f"{img_id} is not a valid image id."
    }