from schemas.package import PackageSchema
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc, Select, Delete
import json

from database.models import Packages, PackageImages

async def db_add_packages(images: UploadFile, data: str, db: Session) -> dict:
    # converting string to object on PackageSchema
    data = PackageSchema.model_validate(json.loads(data))

    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"} 
    image_ids = []
    if images:
        # TODO: Implement a for loop for multiple image
        ## currently take only one image.
        ### swagger UI does not support multiple file selection.
        
        if images.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                    status_code=400,
                    detail=f"{images.filename} is not a supported image"
                )
        # TODO: Implement a for loop for each image

        image_byte = await images.read()

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


