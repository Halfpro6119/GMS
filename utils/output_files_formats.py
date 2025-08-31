from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from utils.google_maps_scraper import GoogleMaps
from output_files_formats import CSVCreator, JSONCreator, XLSXCreator

def run_single_scrape(query, file_lock):
    scraper = GoogleMaps(headless=True, verbose=True, print_lock=file_lock)
    # Assume start_scrapper returns a dict or a list of dicts
    result = scraper.start_scrapper(query)
    # Make sure data is a list of dicts
    if result is None:
        print(f"No data found for query: {query}")
        return
    if isinstance(result, dict):
        data = [result]
    else:
        data = result
    # Save to all formats
    CSVCreator(file_lock).create(data)
    JSONCreator(file_lock).create(data)
    XLSXCreator(file_lock).create(data)
    print(f"Saved results for query: {query}")

if __name__ == '__main__':
    file_lock = Lock()
    with open('queries.txt', 'r', encoding='utf-8') as f:
        queries = [line.strip() for line in f if line.strip()]

    max_workers = 3

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(run_single_scrape, query, file_lock)
            for query in queries
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")
