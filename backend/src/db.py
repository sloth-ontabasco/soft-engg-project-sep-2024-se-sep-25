from .config import MONGO_URI
import mongoengine
import os

db  = mongoengine 
# db.connect(db='SE2024-25-Cluster0',host=MONGO_URI)

def connect_db():
    if os.getenv('FLASK_ENV') == 'testing':  # Check if running in test environment
        db.connect(db='test_db', host='mongomock://localhost')  # Use mongomock for testing
    else:
        db.connect(db='SE2024-25-Cluster0', host=MONGO_URI)

connect_db()  # Call the connect_db function to establish the connection
