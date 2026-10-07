from sqlalchemy.orm import Session
from sqlalchemy import exc, Select
import base64

from database.models import PackageImages, Categories, Destinations

async def db_task_get_imagebin_from_id(image_ids: list[int], db: Session) -> list:
    image_bins = []

    for image_id in image_ids:
        stmt = Select(PackageImages.image_bin, PackageImages.mime_type).where(PackageImages.id == image_id)
        image_bin = db.execute(stmt).first()
        
        if image_bin is None:
            continue
        image_base64 = base64.b64encode(image_bin[0]).decode("utf-8")
        image_b64_url = f"data:{image_bin[1]};base64,{image_base64}"
        image_bins.append(image_b64_url)

    return image_bins

async def db_task_get_category_from_id(cat_ids: list[int], db:Session) -> list:
    categories = []

    for cat_id in cat_ids:
        stmt = Select(Categories.category_text).where(Categories.id == cat_id)
        category = db.execute(stmt).first()

        if category is None:
            continue

        categories.append(category[0])
    return categories


async def db_task_get_destination_from_id(des_ids: list[int], db: Session) -> list:
    destinations = []

    for des_id in des_ids:
        stmt = Select(Destinations.destination_text).where(Destinations.id == des_id)
        destination = db.execute(stmt).first()

        if destination is None:
            continue

        destinations.append(destination[0])

    return destinations