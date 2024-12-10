from open_alex_scraper import OpenAlexScraper
from dotenv import load_dotenv
import os
import asyncio


async def main():

    """
    Main function to scrape papers from OpenAlex API
    Automate the process of scraping papers from OpenAlex API
    and save the results to a JSON file or MongoDB
    """
    load_dotenv()
    MONGO_URL = os.getenv("MONGO_URL")
    openAlexScraper = OpenAlexScraper(mongo_uri=MONGO_URL)
    keywords = []
    save_path = "scraped_papers_random_2.json"
    target_count = 100
    # Scrape papers in a random manner
    filtered_papers = openAlexScraper.scrape_papers(
        keyword_ids=keywords, ignore_issns=True, target_count=target_count, 
        save_to_file=False, save_to_mongo=True, per_page=100,
    )
    print(f"Found {len(filtered_papers)} papers with new ISSNs")

    return filtered_papers

if __name__ == "__main__":
    asyncio.run(main())