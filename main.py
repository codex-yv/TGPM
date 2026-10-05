from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text


from database.configs import REDIS, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials= True,
    allow_headers=['*'],
    allow_methods=['*'],
)

@app.get("/health")
def getServerHealth():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            pg = True

    except Exception as e:
        pg = False

    try:
        r = REDIS.ping()
    except Exception as e:
        r = False

    return {
        "server_status": "UP",
        "redis_Status": "UP" if r else "DOWN",
        "pg_status": "UP" if pg else "DOWN"
    }