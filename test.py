import sys
import json

def main():
    # Check if JSON data is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 test.py <json_data>")
        sys.exit(2)

    # Retrieve JSON data from command-line argument
    json_data_str = sys.argv[1]

    try:
        # Parse JSON data
        json_data = json.loads(json_data_str)
        print("Received JSON data:")
        print(json.dumps(json_data, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()

