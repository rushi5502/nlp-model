# mongodb_connection.py
from pymongo import MongoClient, errors

# Define your MongoDB URI
MONGO_URI = "mongodb+srv://Mayur:Mayur2002@cluster0.cemqecf.mongodb.net/InterShipPortal?retryWrites=true&w=majority&appName=Cluster0"

def get_db():
    """
    Connects to MongoDB and returns the database object.
    """
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')  # Check the connection
        print("Database connected successfully.")
        db = client['InterShipPortal']
        return db
    except errors.ServerSelectionTimeoutError as err:
        print(f"Database connection failed: {err}")
        return None
