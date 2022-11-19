from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

from routes import router as list_router

config = dotenv_values(".env")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API using Fast API and pymongo"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(list_router, tags=["list"], prefix="/list")
