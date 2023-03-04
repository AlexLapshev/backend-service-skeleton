import os


class Config:
    DEBUG: bool = os.getenv("DEBUG").lower() == "true"
    HOST: str = os.getenv("APP_HOST")
    PORT: int = os.getenv("APP_PORT")
    DATABASE_URI: str = (
        f"postgres://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
