import os


class Settings:

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@postgres:5432/costdb"
    )


settings = Settings()