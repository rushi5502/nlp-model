from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGODB_URI")

def get_db():
    """
    Connects to MongoDB and returns the database object.
    """
    try:
        if MONGO_URI is None:
            raise ValueError("MONGODB_URI environment variable not set")

        client = MongoClient(MONGO_URI)
        client.admin.command('ping')  # Check the connection
        print("Database connected successfully.")
        db = client['InterShipPortal']
        return db
    except ValueError as ve:
        print(ve)
        return None
    except errors.ServerSelectionTimeoutError as err:
        print(f"Database connection failed: {err}")
        return None
