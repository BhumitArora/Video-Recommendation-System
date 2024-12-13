from config import API_ENDPOINTS, HEADERS, PAGE_SIZE
from fetcher.api_fetcher import fetch_data
from fetcher.storage import save_data_to_file

def main():
    for key, endpoint in API_ENDPOINTS.items():
        print(f"Fetching data for {key} posts...")
        data = fetch_data(api_url=endpoint, headers=HEADERS, page_size=PAGE_SIZE)
        file_name = f"data_{key}.json"
        save_data_to_file(data, file_name)

if __name__ == "__main__":
    main()
