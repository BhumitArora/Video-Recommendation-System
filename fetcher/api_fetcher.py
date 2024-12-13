import json
import requests
from fetcher.utils import log_message

def fetch_data(api_url, headers, page_size):
    page = 1
    fetched_ids = set()  # To store unique IDs
    all_data = []

    while True:
        log_message(f"Fetching page {page} from {api_url}...")
        params = {"page": page, "page_size": page_size}
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code != 200:
            log_message(f"Error {response.status_code}: {response.text}")
            break

        # Inspect raw response
        raw_content = response.content
        print(f"Raw response from page {page}: {raw_content}")

        try:
            # Decode the content (if bytes) and load as JSON
            decoded_content = raw_content.decode("utf-8") if isinstance(raw_content, bytes) else raw_content

            # Parse the string into JSON
            parsed_json = json.loads(decoded_content)

            if isinstance(parsed_json, dict):
                # Print all top-level keys in the JSON object
                log_message(f"Top-level keys: {list(parsed_json.keys())}")
                
                # Choose the first key that contains a list as its value
                for key, value in parsed_json.items():
                    if isinstance(value, list):
                        data = value
                        log_message(f"Using data from key: '{key}'")
                        break
                else:
                    log_message("No list found in top-level keys.")
                    break

            elif isinstance(parsed_json, list):
                # Root is already a list
                data = parsed_json
            else:
                log_message("Unexpected JSON structure.")
                break

            # Check if data is empty
            if not data:
                log_message("No more data to fetch.")
                break

            # Filter for unique items
            unique_data = [item for item in data if item.get('id') not in fetched_ids]
            fetched_ids.update(item.get('id') for item in unique_data)
            all_data.extend(unique_data)

            # Stop if fewer items than page_size are returned
            if len(data) < page_size:
                break

            page += 1

        except json.JSONDecodeError as e:
            log_message(f"Error parsing JSON string: {e}")
            break
        except Exception as e:
            log_message(f"Error processing response: {e}")
            break

    log_message(f"Total records fetched: {len(all_data)}")
    return all_data
