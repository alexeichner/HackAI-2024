import sys
import json

def main():
    # Check if JSON data is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Error: Please provide JSON data as a command-line argument.")
        sys.exit(1)

    try:
        # Parse the JSON data
        input_data = json.loads(sys.argv[1])

        # Print the JSON data to the console
        print("Received JSON data:")
        print(json.dumps(input_data, indent=2))

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
