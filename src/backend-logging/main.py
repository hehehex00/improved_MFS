import os
import uuid
from datetime import datetime
from typing import Dict

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize Elasticsearch client
es = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://toolbox-elasticsearch:9200"))

app = FastAPI()
INDEX_NAME = "logs"

# Define SQLAlchemy base model

# # Define database models
# class Identity(Base):
#     __tablename__ = "identities"
#     sub = Column(String, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     preferred_username = Column(String, nullable=False)
#     given_name = Column(String, nullable=False)
#     family_name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)

# class Activity(Base):
#     __tablename__ = "activities"
#     id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
#     sub = Column(String, ForeignKey("identities.sub"), nullable=False)
#     activity = Column(Text, nullable=False)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic models for request validation
class ActivityLog(BaseModel):
    identity: Dict[str, str]  # Identity information
    activity: str  # Activity string

# Endpoint to log activity
@app.post("/log_activity")
async def log_activity(log: ActivityLog):
    """Logs an activity and identity into respective tables."""
    identity_data = log.identity
    activity_data = log.activity

    # Prepare the document for Elasticsearch
    item = {
        "identity": identity_data,
        "activity": activity_data,
        "timestamp": datetime.utcnow(),
    }
    
    # Insert into Elasticsearch
    try:
        es.index(index=INDEX_NAME, id=str(uuid.uuid4()), document=item)
        print("success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing in Elasticsearch: {e}")
    
    # Insert the activity into the database
    
    return {"message": "Activity and identity logged successfully"}
