import os

from dotenv import load_dotenv

load_dotenv()


class LocalDBConfig:
    pass


class RemoteDBConfig:
    pass


class MongoDBConfig:
    USERNAME = os.environ.get("MONGO_USERNAME") or "just_for_dev"
    PASSWORD = os.environ.get("MONGO_PASSWORD") or "password_for_dev"
    HOST = os.environ.get("MONGO_HOST") or "localhost"
    PORT = os.environ.get("MONGO_PORT") or "27017"
    TOKEN_MONGO_URL =  os.environ.get("TOKEN_MONGO_URL") or ""
    MONGO_URL = os.environ.get("MONGO_URL") or ""
    BRICHER_MAIN_URL = os.environ.get("BRICHER_MAIN_URL") or ""
    BRICHER_TEST_URL = os.environ.get("BRICHER_TEST_URL") or ""
    DATABASE = "token_database"
    BLOCKCHAIN_SPACE_DB = 'blockchain-space'
    BRICHER_DB = 'BRicher'

if __name__ == "__main__":
    pass
