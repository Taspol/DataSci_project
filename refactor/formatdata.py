import os
import json
import pandas as pd
from tqdm import tqdm


def ensure_list(variable):
    """Ensure the given variable is a list. If it's a dict, convert it to a list containing that dict.
    If it's not a list or dict, return an empty list."""
    if isinstance(variable, dict):
        return [variable]
    elif not isinstance(variable, list):
        return []
    return variable


def extract_coredata(coredata):
    """Extract and flatten core data fields."""
    coredata_flat = coredata.copy()
    # Handle `dc:creator` field
    creator_info = coredata_flat.get('dc:creator', {}).get('author', [{}])[0]
    coredata_flat['creator_given_name'] = creator_info.get(
        'ce:given-name', 'N/A')
    coredata_flat['creator_surname'] = creator_info.get('ce:surname', 'N/A')
    coredata_flat['creator_auid'] = creator_info.get('@auid', 'N/A')

    # Handle `link` field
    coredata_flat['link_self'] = next(
        (link['@href'] for link in coredata.get('link', []) if link['@rel'] == 'self'), 'N/A')
    coredata_flat['link_scopus'] = next(
        (link['@href'] for link in coredata.get('link', []) if link['@rel'] == 'scopus'), 'N/A')

    coredata_flat.pop('dc:creator', None)
    coredata_flat.pop('link', None)
    return coredata_flat


def get_keywords(record_data):
    """Extract author keywords."""
    auth_keywords = record_data.get(
        "abstracts-retrieval-response", {}).get("authkeywords", {})
    if auth_keywords:
        keywords = auth_keywords.get("author-keyword", [])
        return "".join(k["$"] + "," for k in keywords).rstrip(",")
    return ""


def extract_author_affiliations(author_group):
    """Extract author affiliations including countries and organizations."""
    countries = ""
    organizations = ""

    for author in ensure_list(author_group):
        affiliation = author.get("affiliation", {})
        country = affiliation.get("country", None)
        organization = affiliation.get("organization", [])

        if country:
            countries += f"{country},"
        for org in ensure_list(organization):
            org_name = org.get("$", None)
            if org_name:
                organizations += f"{org_name},"

    return countries.rstrip(","), organizations.rstrip(",")


def extract_funding_agencies(funding_list):
    """Extract funding agencies."""
    funding_agencies = ""
    for funding in ensure_list(funding_list):
        funding_agency = funding.get(
            "xocs:funding-agency-matched-string", None)
        if funding_agency:
            funding_agencies += f"{funding_agency},"
    return funding_agencies.rstrip(",")


def process_record(file_path):
    """Process a single record and return a formatted dictionary."""
    try:
        with open(file_path, 'r') as file:
            record_data = json.load(file)

        coredata = record_data['abstracts-retrieval-response']['coredata']
        author_group = record_data.get('abstracts-retrieval-response', {}).get(
            'item', {}).get('bibrecord', {}).get("head", {}).get("author-group", [])
        funding_list = record_data.get('abstracts-retrieval-response', {}).get(
            'item', {}).get('xocs:meta', {}).get("xocs:funding-list", {}).get("xocs:funding", [])

        countries, organizations = extract_author_affiliations(author_group)
        funding_agencies = extract_funding_agencies(funding_list)
        auth_keywords = get_keywords(record_data)

        formatted = extract_coredata(coredata)
        data_summary = {
            "Countries": countries,
            "Organizations": organizations,
            "Funding Agencies": funding_agencies,
            "auth-keywords": auth_keywords
        }
        formatted.update(data_summary)
        return formatted

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def process_year(folder_path, year):
    """Process all records for a given year."""
    records = os.listdir(folder_path)
    coredata_list = []

    for record in tqdm(records, desc=f"Processing records for year {year}"):
        file_path = os.path.join(folder_path, record)
        formatted_data = process_record(file_path)
        if formatted_data:
            coredata_list.append(formatted_data)

    return coredata_list


def save_to_csv(data, year):
    """Save processed data to a CSV file."""
    if data:
        df_coredata = pd.DataFrame(data)
        output_file_path = f"processed_data_{year}.csv"
        df_coredata.to_csv(output_file_path, index=False)
        print(f"DataFrame saved to {output_file_path}")
    else:
        print(f"No data to save for year {year}.")


def add_json_extension(file_path):
    """Add json extension to the file path whole dir execept .DS_Store"""
    for file in os.listdir(file_path):
        file_path = os.path.join(file_path, file)
        if not file_path.endswith(".DS_Store"):
            return file_path + ".json"


def process_project_data(project_path="Project/"):
    """Main function to process JSON files in the specified directory."""
    data_dir = os.listdir(project_path)
    data_dir
    for year in data_dir:
        folder_path = os.path.join(project_path, year)
        data = process_year(folder_path, year)
        save_to_csv(data, year)


def main():
    PROJECT_PATH = "Project/"
    add_json_extension(PROJECT_PATH)
    process_project_data(PROJECT_PATH)


if __name__ == "__main__":
    main()
