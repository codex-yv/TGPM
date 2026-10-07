from schemas.package import PackageSchema
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc, Select, Delete, Update
from typing import List
import json

from database.models import Packages, PackageImages, Categories, Destinations

from schemas.package import CategorySchema, DestinationSchema

async def db_add_packages(images: List[UploadFile], data: str, db: Session) -> dict:
    # converting string to object on PackageSchema
    data = PackageSchema.model_validate(json.loads(data))

    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"} 
    image_ids = []
    if images:
        for image in images:
            if image.content_type not in ALLOWED_TYPES:
                raise HTTPException(
                        status_code=400,
                        detail=f"{image.filename} is not a supported image"
                    )

            image_byte = await image.read()

            image_model = PackageImages(
                image_bin = image_byte
            )

            db.add(image_model)
            db.flush()

            image_ids.append(image_model.id)

    if not data.image_id:
        data.image_id = image_ids
    else:
        # TODO: check if image id in data.image_id exist
        data.image_id = list(set(data.image + image_ids))


    package_model = Packages(
        package_name = data.package_name.lower().strip().replace(' ', '_'),
        destination_id = str(data.destination_id), # TODO: Check if destination_id exist
        description = data.description,
        duration = data.duration,
        price = data.price,
        category_id = str(data.category_id), # TODO: check if category id exist
        itinerary = str(data.itinerary),
        inclusions = str(data.inclusions),
        exclusions = str(data.exclusions),
        image_id = str(data.image_id),
    )
    try:
        db.add(package_model)
        db.commit()
        db.refresh(package_model)

    except exc.IntegrityError:
        db.rollback()

        return {
            "status":False,
            "message": "dupicate",
            "data": None
        }

    return {
        "status":True,
        "message": "Inserted",
        "data": package_model.id

    }


async def db_add_new_category(data: CategorySchema, db: Session) -> dict:
    category_model = Categories(
        category_text = data.category
    )

    try:
        db.add(category_model)
        db.commit()
        db.refresh(category_model)
    except exc.IntegrityError:
        db.rollback()

        return {
            "status":False,
            "message": "dupicate category",
            "data": None
        }
    return {
        "status":True,
        "message": "Created new category.",
        "data": category_model.id
    }


async def db_add_new_destination(data: DestinationSchema, db: Session) -> dict:
    destination_model = Destinations(
        destination_text = data.destination_text
    )

    try:
        db.add(destination_model)
        db.commit()
        db.refresh(destination_model)
    except exc.IntegrityError:
        db.rollback()

        return {
            "status":False,
            "message": "dupicate destination",
            "data": None
        }
    return {
        "status":True,
        "message": "Created new destination.",
        "data": destination_model.id
    }

async def db_toggle_package_status(data: int, db: Session):
    stmt = Select(Packages.status).where(Packages.id == data)

    result = db.execute(stmt).scalar_one_or_none()

    if result == None:
        return {
            "status": False,
            "message": f"ID: {data} not found in packages relation. ",
            "data": None
        }
    
    new_status = not result
    upd_stmt = Update(Packages).where(Packages.id == data).values(status = new_status)
    db.execute(upd_stmt)
    db.commit()

    return {
        "status": True,
        "message": f"Package status toggled!",
        "data": new_status
    }
    