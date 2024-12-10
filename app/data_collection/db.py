import pymongo
from dotenv import load_dotenv
import os
import json
import pandas as pd
from typing import List


class MongoDBHandler:
    """
    A class to handle MongoDB operations.
    """

    def __init__(self):
        """
        Initialize the MongoDBHandler by loading the MongoDB URL from the .env file.
        """
        load_dotenv()
        self.mongo_url = os.getenv("MONGO_URL")
        if not self.mongo_url:
            raise ValueError("MONGO_URL not found in the .env file.")
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client['dsde']

    def get_all_data(self, limit: int = 100):
        """
        Fetch all data from MongoDB.

        :param limit: Number of records to fetch.
        :return: Tuple of lists containing data from 'openAlex_data' and 'data' collections.
        """
        openalex_data = self.db['openAlex_data'].find(limit=limit)
        data = self.db['data'].find(limit=limit)
        return list(openalex_data), list(data)

    def upload_json_csv_to_mongo(self, file_path: str, collection_name: str):
        """
        Upload a JSON or CSV file to MongoDB.

        :param file_path: Path to the JSON or CSV file.
        :param collection_name: The name of the collection to upload the data to.
        """
        try:
            collection = self.db[collection_name]
            if file_path.endswith(".json"):
                with open(file_path, "r") as f:
                    data = json.load(f)
                    collection.insert_many(data)
                    print(f"Successfully uploaded {len(data)} records to MongoDB.")
            elif file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
                data = df.to_dict(orient="records")
                collection.insert_many(data)
                print(f"Successfully uploaded {len(data)} records to MongoDB.")
            else:
                raise ValueError("File format not supported. Use JSON or CSV.")
        except Exception as e:
            print(f"Error uploading file to MongoDB: {e}")

    def upload_data_to_mongo(self, data: List[dict], collection_name: str):
        """
        Upload data to MongoDB.

        :param data: List of dictionaries to upload.
        :param collection_name: The name of the collection to upload the data to.
        """
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries.")
        try:
            collection = self.db[collection_name]
            collection.insert_many(data)
            print(f"Successfully uploaded {len(data)} records to MongoDB.")
        except Exception as e:
            print(f"Error uploading data to MongoDB: {e}")

