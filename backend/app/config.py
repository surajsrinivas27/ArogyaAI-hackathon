from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = "ArogyaAI"

    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "arogyaai")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()