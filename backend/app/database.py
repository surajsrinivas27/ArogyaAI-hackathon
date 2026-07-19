from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
database = None


async def connect_to_mongo():
    global client, database

    client = AsyncIOMotorClient(settings.MONGODB_URI)

    database = client[settings.DATABASE_NAME]

    await client.admin.command("ping")

    print("✅ MongoDB Connected")


async def close_mongo_connection():
    global client

    if client:
        client.close()
        print("🔴 MongoDB Connection Closed")