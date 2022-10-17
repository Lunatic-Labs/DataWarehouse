import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_lunatic_labs_key")
    DEBUG = False


# different config objects allow us to run the application in different
# modes, such as testing, development, production... etc.
class DevelopmentConfig(Config):
    # env vars here
    DATABASE_URL = os.environ.get("DATABASE_URL")

    DEBUG = True
