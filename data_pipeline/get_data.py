import pymongo
from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
from typing import List

def get_mongo_url():
    """
    Load MongoDB URL from .env file
    """
    load_dotenv()
    MONGO_URL = os.getenv("MONGO_URL")
    return MONGO_URL

def get_all(limit: int = 100, ):
    """
    Fetch all data from MongoDB
    Note: openAlex_data and data structures are different
    """
    MONGO_URL = get_mongo_url()
    client = pymongo.MongoClient(MONGO_URL)
    openAlex_data = client['dsde']['openAlex_data'].find(limit=limit)
    data = client['dsde']['data'].find(limit=limit)
    
    return openAlex_data, data