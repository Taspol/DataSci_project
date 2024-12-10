from typing import List
import requests
import json


class OpenAlexScraper:
    def __init__(self, base_url="https://api.openalex.org/works"):
        self.base_url = base_url
        self.scraped_issns = self.load_scraped_issns()

    def load_scraped_issns(self, file_path="issns.json"):
        try:
            with open(file_path, "r") as f:
                issns = json.load(f)
                print(f"Loaded {len(issns)} scraped ISSNs from {file_path}")
                return issns
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def fetch_papers(self, keyword_ids: List[str], year: int, page=1, per_page=100):
        keyword_ids = [f"keywords/{kw}" for kw in keyword_ids]
        keyword_ids = "|".join(keyword_ids)
        filter_string = (
            f"open_access.is_oa:true,"
            f"keywords.id:{keyword_ids}" if keyword_ids else ""
            f"publication_year:{year}" if year else ""
        )
        params = {
            "page": page,
            "filter": filter_string,
            "per_page": per_page,
            "sort": "publication_year:desc"
        }

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(response.text)
                return {"error": f"Failed to retrieve data, status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    def save_file(self, file_path: str, data):
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Scraped data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")

    def scrape_papers(self, keyword_ids: List[str], year: int, per_page=200, ignore_issns=False, target_count=None, save_path=None):
        all_filtered_papers = []
        page = 1
        total_collected = 0

        while True:
            # Fetch papers from OpenAlex API
            papers_data = self.fetch_papers(
                keyword_ids=keyword_ids, year=year, page=page, per_page=per_page
            )

            # Check if the fetch was successful
            if "results" not in papers_data:
                print(
                    f"Error fetching papers: {papers_data.get('error', 'Unknown error')}")
                break

            # Filter papers based on ISSNs if needed
            filtered_papers = []
            if not ignore_issns:
                filtered_papers = papers_data["results"]
            else:
                for paper in papers_data["results"]:
                    try:
                        issns = paper["primary_location"]["source"].get(
                            "issn", [])
                        # Check if none of the ISSNs in this paper are already scraped
                        if not any(issn in self.scraped_issns for issn in issns):
                            filtered_papers.append(paper)
                    except (KeyError, AttributeError, TypeError):
                        # Skip papers without ISSNs or primary_location/source data
                        continue

            # Add filtered papers to the main list
            all_filtered_papers.extend(filtered_papers)
            total_collected += len(filtered_papers)

            # Check if the target count is reached
            if target_count and total_collected >= target_count:
                print(
                    f"Target of {target_count} papers reached. Stopping scrape.")
                break

            # Check if there are more pages
            total_papers = papers_data.get("meta", {}).get("count", 0)
            total_pages = (total_papers + per_page - 1) // per_page
            print(
                f"Page {page}/{total_pages} fetched, {total_collected} papers collected so far.")

            if page >= total_pages:
                break

            page += 1

        # Trim the result if over the target count
        if target_count:
            all_filtered_papers = all_filtered_papers[:target_count]

        # Save to JSON file if save_path is provided
        if save_path:
            self.save_file(save_path, all_filtered_papers)

        return all_filtered_papers


if __name__ == "__main__":
    openAlexScraper = OpenAlexScraper()
    # keywords = ["machine-learning", "treatment"]
    keywords = []
    SAVE_PATH = "scraped_papers.json"
    # Scrape papers in one step
    filtered_papers = openAlexScraper.scrape_papers(
        keyword_ids=keywords, year=2024, ignore_issns=True, target_count=100, save_path=SAVE_PATH
    )
    print(f"Found {len(filtered_papers)} papers with new ISSNs")
