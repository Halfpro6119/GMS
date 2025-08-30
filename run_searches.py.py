from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.google_maps_scraper import GoogleMaps

def run_single_scrape(query):
    # Adjust your GoogleMaps constructor as needed
    scraper = GoogleMaps(headless=True, verbose=True)
    scraper.start_scrapper(query)

if __name__ == '__main__':
    # Read your queries from a text file, one per line
    with open('queries.txt', 'r', encoding='utf-8') as f:
        queries = [line.strip() for line in f if line.strip()]

    max_workers = 3  # Number of parallel searches

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all jobs to the executor
        future_to_query = {executor.submit(run_single_scrape, query): query for query in queries}
        for future in as_completed(future_to_query):
            query = future_to_query[future]
            try:
                future.result()
                print(f"Finished: {query}")
            except Exception as exc:
                print(f"{query} generated an exception: {exc}")