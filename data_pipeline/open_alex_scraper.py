from typing import List
import requests
import json
import pandas as pd
import pymongo
import os


class OpenAlexScraper:
    def __init__(self, mongo_uri: str, base_url="https://api.openalex.org/works"):
        self.base_url = base_url
        self.mongo_uri = mongo_uri
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.openAlex_data_collection = self.client['dsde']['openAlex_data']
        self.data = self.client['dsde']['data']
        self.scraped_issns = self.load_scraped_issns()

    def load_scraped_issns(self, file_path="issns.json"):
        try:
            # Fetch distinct ISSNs from MongoDB
            issns = set(self.openAlex_data_collection.distinct(
                'primary_location.source.issn'))
            data_issns = set(self.data.distinct('prism:isbn'))
            issns.update(data_issns)
            # Optionally load from file if it exists
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    file_issns = set(json.load(f))
                    issns.update(file_issns)
                    print(f"Loaded {len(file_issns)} ISSNs from {file_path}")

            print(f"Loaded {len(issns)} total ISSNs (MongoDB + file)")
            return issns

        except Exception as e:
            print(f"Error loading ISSNs: {e}")
            return set()

    def fetch_papers(self, filter_string: str, sample_size: int, per_page: int):
        params = {
            "filter": filter_string,
            "sample": sample_size,
            "per-page": per_page,
        }

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.text}")
                return {"error": f"Failed to retrieve data, status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    def transform_data(self, data: List[dict]) -> List[dict]:
        df = pd.DataFrame(data)
        columns_to_keep = [
            'title', 'fwci', 'cited_by_count', 'type', 'type_crossref', 'topics',
            'locations', 'locations_count', 'primary_topic', 'concepts',
            'relevance_score', 'publication_date', 'authorships',
            'publication_year', 'language', 'abstract_inverted_index',
            'referenced_works', 'apc_list', 'apc_paid'
        ]

        df = df[columns_to_keep]
        return df.to_dict(orient="records")

    def save_file(self, file_path: str, data):
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Scraped data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")

    def save_to_mongo(self, data: List[dict]):
        try:
            transformed_data = self.transform_data(data)
            self.openAlex_data_collection.insert_many(transformed_data)
            print(f"Scraped data saved to MongoDB")
        except Exception as e:
            print(f"Error saving data to MongoDB: {e}")

    def scrape_papers(self, keyword_ids: List[str], per_page=200,
                      ignore_issns=False, target_count=None, save_path=None,
                      save_to_file=None, save_to_mongo=True
                      ):
        all_filtered_papers = []
        total_collected = 0

        # Build filter string
        keyword_filters = [f"keywords/{kw}" for kw in keyword_ids]
        keyword_filter_string = "|".join(
            keyword_filters) if keyword_filters else ""
        filter_string = "open_access.is_oa:true,language:en"
        if keyword_filter_string:
            filter_string += f",keywords.id:{keyword_filter_string}"

        print(f"Filter string: {filter_string}")

        while total_collected < target_count:
            papers_data = self.fetch_papers(
                filter_string=filter_string, sample_size=per_page, per_page=per_page
            )

            if "results" not in papers_data:
                print(
                    f"Error fetching papers: {papers_data.get('error', 'Unknown error')}")
                continue

            # Filter papers based on ISSNs if needed
            filtered_papers = []
            if ignore_issns:
                filtered_papers = papers_data["results"]
            else:
                for paper in papers_data["results"]:
                    try:
                        issns = paper["primary_location"]["source"].get(
                            "issn", [])
                        if not any(issn in self.scraped_issns for issn in issns):
                            filtered_papers.append(paper)
                    except (KeyError, AttributeError, TypeError):
                        continue

            all_filtered_papers.extend(filtered_papers)
            total_collected += len(filtered_papers)

            if total_collected >= target_count:
                print(
                    f"Target of {target_count} papers reached. Stopping scrape.")
                break

            print(f"Collected {total_collected} papers so far.")

        all_filtered_papers = all_filtered_papers[:target_count]
        if save_to_mongo:
            self.save_to_mongo(all_filtered_papers)
        if save_path and save_to_file:
            self.save_file(save_path, all_filtered_papers)

        return all_filtered_papers
