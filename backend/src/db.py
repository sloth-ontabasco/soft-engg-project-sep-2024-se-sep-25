from .config import MONGO_URI
import mongoengine


db  = mongoengine 
db.connect(db='SE2024-25-Cluster0',host=MONGO_URI)
