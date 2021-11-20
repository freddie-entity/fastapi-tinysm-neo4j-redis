from pydantic import BaseSettings
import os

class CommonSettings(BaseSettings):
    APP_NAME: str = os.environ.get("APP_NAME", "TINYSM")
    DEBUG_MODE: bool = os.environ.get("DEBUG_MODE", True)
    FILE_PATH: str = os.environ.get("FILE_PATH", './static/images/')
    SECRET: str = os.environ.get("SECRET", "2839fhd2i9dh2i3d289ncdow90c283dfhsiu13dbfskdjb")
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME", "orenbeworldwide@gmail.com")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD", 'extbrsvhzwguzmms')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15)


class ServerSettings(BaseSettings):
    HOST: str = os.environ.get("HOST", "localhost")
    PORT: int = os.environ.get("PORT", 8000)
    EXTERNAL_HOST: str = os.environ.get("EXTERNAL_HOST", "localhost")
    EXTERNAL_PORT: int = os.environ.get("EXTERNAL_PORT", 3000)
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", 'redis://localhost:6379')
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", 'redis://localhost:6379')

class DatabaseSettings(BaseSettings):
    DB_MONGO_URL: str = os.environ.get("DB_MONGO_URL", 'mongodb+srv://tinysm:220641@cluster0.qt8ln.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    DB_MONGO_NAME: str = os.environ.get("DB_MONGO_NAME", 'TINYSM')
    DB_NEO4J_HOST: str = os.environ.get("DB_NEO4J_HOST", 'neo4j+s://7d3a98ad.databases.neo4j.io')
    DB_NEO4J_PASSWORD: str = os.environ.get("DB_NEO4J_PASSWORD", '_wRWdbAmGiRvGhcSGLeqXLOJBX395g30oxaWr5cD6Is')
    DB_NEO4J_USERNAME: str = os.environ.get("DB_NEO4J_USERNAME", 'neo4j')
    DB_REDIS_CACHE: str = os.environ.get("DB_REDIS_CACHE", 'redis://localhost:6379')


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
