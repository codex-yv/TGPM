from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import redis


load_dotenv()

POSTGRES_URL = os.getenv('POSTGRES_URL')
REDIS_URL = os.getenv('REDIS_URL')

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)
Base = declarative_base()


REDIS = redis.Redis.from_url(
    REDIS_URL,
    socket_connect_timeout=2
    
)

