from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, Double, Sequence
from database.configs import Base

class Packages(Base):
    __tablename__ = 'packages'

    id = Column(Integer, Sequence("package_id_seq", start=1000), primary_key = True, index = True)
    package_name = Column(String, unique = True, index = True)
    destination_id = Column(String, index = True) # FORMAT: "[107, 113, ...]"
    description  = Column(String)
    duration = Column(Integer, index = True)
    price = Column(Double, index = True)
    category_id = Column(String) # FORMAT: "[107, 113, ...]"
    itinerary = Column(String) # FORMAT: "{1: [t1, t2, t3, ...], 2: [t1, t2, ...]}"
    inclusions = Column(String) # FORMAT: "[i1, i2, i3, ...]"
    exclusions = Column(String) # FORMAT: "[e1, e2, e3, ...]"
    image_id = Column(String) # FORMAT: "[101, 103, ...]"
    status = Column(Boolean, default = True)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence("category_seq_id", start = 100), primary_key = True, index = True)
    category_text = Column(String)

class Destinations(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, Sequence("category_seq_id", start = 100), primary_key = True, index = True)
    category_text = Column(String)

    destination_text = Column(String, index = True)

# we can use cloud to store images use their urls (good for production)
# eg. Cloudinary
# currently storing in db as binary
class PackageImages(Base):
    __tablename__ = 'images'
    id  = Column(Integer, Sequence("category_seq_id", start = 100), primary_key = True, index = True)
    image_bin = Column(LargeBinary) 
