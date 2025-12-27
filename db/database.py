import motor.motor_asyncio
import os  
from dotenv import load_dotenv
load_dotenv()

mongo_url=os.getenv("MONGO_URL")
client=motor.motor_asyncio.AsyncIOMotorClient(
    mongo_url,
    )

db=client.resume_analyzer
resumes_collection=db.resumes
auth_collection=db.auth

async def save_resume_data(data: dict):
    result = await resumes_collection.insert_one(data)
    return result.inserted_id

