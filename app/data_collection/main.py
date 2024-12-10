from open_alex_scraper import OpenAlexScraper
import os
import asyncio


async def main():
    """
    Main function to scrape papers from OpenAlex API
    Automate the process of scraping papers from OpenAlex API
    and save the results to a JSON file or MongoDB
    """

    openAlexScraper = OpenAlexScraper()

    keywords = []
    save_path = "./data/scraped_papers_random2.json"
    target_count = 100
    # Scrape papers in a random manner
    filtered_papers = openAlexScraper.scrape_papers(
        keyword_ids=keywords,
        target_count=target_count,
        save_to_file=True,
        save_to_mongo=True,
        save_path=save_path
    )
    print(f"Found {len(filtered_papers)} papers with new ISSNs")

    return filtered_papers

if __name__ == "__main__":
    asyncio.run(main())
