import json

def save_data_to_file(data, file_name):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_name}")

def load_data_from_file(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
