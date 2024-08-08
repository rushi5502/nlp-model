from pymongo import MongoClient, errors
import os

# Fetch MongoDB URI from environment variables
MONGO_URI = os.getenv("mongodb+srv://Mayur:Mayur2002@cluster0.cemqecf.mongodb.net/InterShipPortal?retryWrites=true&w=majority&appName=Cluster0"
)

def get_db():
    """
    Connects to MongoDB and returns the database object.
    """
    try:
        if MONGO_URI is None:
            raise ValueError("MONGO_URI environment variable not set")

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
