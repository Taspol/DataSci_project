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

def get_all_data(limit: int = 100):
    """
    Fetch all data from MongoDB
    Note: openAlex_data and data structures are different
    """
    MONGO_URL = get_mongo_url()
    client = pymongo.MongoClient(MONGO_URL)
    openAlex_data = client['dsde']['openAlex_data'].find(limit=limit)
    data = client['dsde']['data'].find(limit=limit)
    
    return list(openAlex_data), list(data)

def upload_json_csv_to_mongo(file_path: str, collection_name: str):
    """
    Upload JSON/CSV file to MongoDB
    """
    MONGO_URL = get_mongo_url()
    client = pymongo.MongoClient(MONGO_URL)
    try:
        collection = client['dsde'][collection_name]
        if file_path.endswith(".json"):
            with open(file_path, "r") as f:
                data = json.load(f)
                collection.insert_many(data)
                print(f"Successfully uploaded {len(data)} records to MongoDB")
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            data = df.to_dict(orient="records")
            collection.insert_many(data)
            print(f"Successfully uploaded {len(data)} records to MongoDB")
        else:
            raise ValueError("File format not supported")
    except Exception as e:
        print(f"Error uploading file to MongoDB: {e}")

def upload_data_to_mongo(data: List[dict], collection_name: str):
    """
    Upload data to MongoDB
    """
    if type(data) != list:
        raise ValueError("Data must be a list of dictionaries")
    MONGO_URL = get_mongo_url()
    client = pymongo.MongoClient(MONGO_URL)
    try:
        collection = client['dsde'][collection_name]
        collection.insert_many(data)
        print(f"Successfully uploaded {len(data)} records to MongoDB")
    except Exception as e:
        print(f"Error uploading data to MongoDB: {e}")
    

__all__ = ["get_mongo_url", "get_all_data", "upload_json_csv_to_mongo", "upload_data_to_mongo"]