from schemas.package import PackageSchema
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc, Select, Delete, Update
from typing import List
import json
import ast

from database.models import Packages, PackageImages, Categories, Destinations

from schemas.package import CategorySchema, DestinationSchema

from utils.tasks import db_task_get_category_from_id, db_task_get_imagebin_from_id, db_task_get_destination_from_id
from utils.validations import db_validate_categories_id, db_validate_destinations_id, db_validate_image_id

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
                image_bin = image_byte,
                mime_type = image.content_type
            )

            db.add(image_model)
            db.flush()

            image_ids.append(image_model.id)

    if not data.image_id:
        data.image_id = image_ids
    else:
        valid_img_id_data = await db_validate_image_id(img_ids= data.image_id, db=db)
        print(valid_img_id_data)
        if not valid_img_id_data['status']:
            return {
                "status":False,
                "message": valid_img_id_data['message'],
                "data": None
            }
        data.image_id = list(set(data.image_id + image_ids))

    #$#  validating destination and category id before inserting in package.
    valid_des_id_data = await db_validate_destinations_id(des_ids= data.destination_id, db=db)
    valid_cat_id_data = await db_validate_categories_id(cat_ids= data.category_id, db=db)
    if not (valid_des_id_data['status'] and valid_cat_id_data['status']) :
        return {
            "status":False,
            "message": valid_des_id_data['message'] if not valid_des_id_data['status'] else valid_cat_id_data['message'],
            "data": None
        }

    package_model = Packages(
        package_name = data.package_name.lower().strip().replace(' ', '_'),
        destination_id = str(data.destination_id),
        description = data.description,
        duration = data.duration,
        price = data.price,
        category_id = str(data.category_id), 
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
    cat_id = []
    for cat in data.category:
        category_model = Categories(
            category_text = cat
        )

        try:
            db.add(category_model)
            db.flush()
            cat_id.append(category_model.id)

        except (exc.IntegrityError):
            db.rollback()

            return {
                "status":False,
                "message": f"Category: {cat} - already exist. ",
                "data": None
            }
        
    db.commit()
    return {
        "status":True,
        "message": "Created new categories.",
        "data": cat_id
    }


async def db_add_new_destination(data: DestinationSchema, db: Session) -> dict:
    des_id = []

    for des in data.destination_text:

        destination_model = Destinations(
            destination_text = des
        )

        try:
            db.add(destination_model)
            db.flush()
            des_id.append(destination_model.id)
        except exc.IntegrityError:
            db.rollback()

            return {
                "status":False,
                "message": f"Destination: {des} - already exist.",
                "data": None
            }
        
    db.commit()
    return {
        "status":True,
        "message": "Created new destination.",
        "data": des_id
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


async def db_get_package_by_package_id(package_id: int, db:Session) -> list | None:
    data = db.query(Packages).filter(Packages.id == package_id).scalar()
    image_bins = await db_task_get_imagebin_from_id(image_ids = ast.literal_eval(data.image_id), db=db)
    categories = await db_task_get_category_from_id(cat_ids= ast.literal_eval(data.category_id), db=db)
    destinations = await db_task_get_destination_from_id(des_ids= ast.literal_eval(data.destination_id), db=db)

    package = {
        "id": data.id,
        "package_name": data.package_name,
        "destinations": destinations,
        "description": data.description,
        "duration": data.duration,
        "price": data.price,
        "categories": categories,
        "itinerary": ast.literal_eval(data.itinerary),
        "inclusions": ast.literal_eval(data.inclusions),
        "exclusions": ast.literal_eval(data.exclusions),
        "images": image_bins,
        "status": data.status,
    }

    return package

async def db_get_all_package(db:Session):
    packages = []
    datas = db.query(Packages).all()
    for data in datas:
        image_bins = await db_task_get_imagebin_from_id(image_ids = ast.literal_eval(data.image_id), db=db)
        categories = await db_task_get_category_from_id(cat_ids= ast.literal_eval(data.category_id), db=db)
        destinations = await db_task_get_destination_from_id(des_ids= ast.literal_eval(data.destination_id), db=db)
        package = {
            "id": data.id,
            "package_name": data.package_name,
            "destinations": destinations,
            "description": data.description,
            "duration": data.duration,
            "price": data.price,
            "categories": categories,
            "itinerary": ast.literal_eval(data.itinerary),
            "inclusions": ast.literal_eval(data.inclusions),
            "exclusions": ast.literal_eval(data.exclusions),
            "images": image_bins,
            "status": data.status,
        }
        packages.append(package)

    return packages
