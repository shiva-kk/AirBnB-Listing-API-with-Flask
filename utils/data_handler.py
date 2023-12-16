import json

DATA_FILE = 'data/airbnb.json'

def read_data():
    try:
        with open('data/airbnb.json', 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except FileNotFoundError:
        print("JSON file not found.")
        return None

def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)
