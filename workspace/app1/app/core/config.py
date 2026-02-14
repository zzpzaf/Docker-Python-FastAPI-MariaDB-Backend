# app/core/config.py 
# (pure driver DSN)
#
# Loads DB connection parameters from environment variables (Docker friendly)

from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Bookstore1 - app1"
    api_prefix: str = "/api"

    # DSN for pymysql.connect()
    db_host: str = os.getenv("DB_HOST", "mariadb")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_name: str = os.getenv("DB_NAME", "bookstore1")


settings = Settings()
