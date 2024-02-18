#This is where we will make the model
import requests
import sys
import json
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def process_json_data(user_dict):

    # new_dict = {"Unnamed": 0}
    # new_dict.update(user_dict)

    # Creating output csv
    csv_file_path = 'output.csv'

    # Create placeholder rows for csv file
    placeholder_row1 = [0, 0, 0, 0, "yes", "yes", "yes", "yes", "yes", 0, "yes", "furnished"]
    placeholder_row2 = [0, 0, 0, 0, "no", "no", "no", "no", "no", 0, "no", "semi-furnished"]
    placeholder_row3 = [0, 0, 0, 0, "yes", "yes", "yes", "yes", "yes", 0, "yes", "unfurnished"]

    # Open csv in write mode
    with open(csv_file_path, 'w', newline="") as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header row
        csv_writer.writerow(user_dict.keys())

        # Write the value row
        csv_writer.writerow(user_dict.values())
        csv_writer.writerow(placeholder_row1)
        csv_writer.writerow(placeholder_row2)
        csv_writer.writerow(placeholder_row3)



def predict():
    training_data = pd.read_csv("HousingDataset.csv")

    #Converting object types to category types
    training_data['mainroad'] = training_data['mainroad'].astype('category')
    training_data['guestroom'] = training_data['guestroom'].astype('category')
    training_data['basement'] = training_data['basement'].astype('category')
    training_data['hotwaterheating'] = training_data['hotwaterheating'].astype('category')
    training_data['airconditioning'] = training_data['airconditioning'].astype('category')
    training_data['prefarea'] = training_data['prefarea'].astype('category')
    training_data['furnishingstatus'] = training_data['furnishingstatus'].astype('category')

    #Do one-hot encoding
    training_data = pd.get_dummies(training_data)
    #This line shows how each categorical data column is now converted to something that can be represented with numbers
    # print(data.columns)

    # Start building a regression model

    # Target variable (What we want to predict)
    y = training_data["price"]

    # Drop the target variable
    x = training_data.drop("price", axis=1)

    # 80/20 split between training and testing
    x_train,x_test,y_train,y_test = train_test_split(
        x,y,
        train_size = 0.80,
        random_state = 1)

    # Create an instance of the linear regression model
    lr = LinearRegression()

    # Build using the training data
    lr.fit(x_train, y_train)

    # Mean squared error
    y_pred = lr.predict(x_test)

    # Model prediction
    user_data = pd.read_csv("output.csv")

    user_data['mainroad'] = user_data['mainroad'].astype('category')
    user_data['guestroom'] = user_data['guestroom'].astype('category')
    user_data['basement'] = user_data['basement'].astype('category')
    user_data['hotwaterheating'] = user_data['hotwaterheating'].astype('category')
    user_data['airconditioning'] = user_data['airconditioning'].astype('category')
    user_data['prefarea'] = user_data['prefarea'].astype('category')
    user_data['furnishingstatus'] = user_data['furnishingstatus'].astype('category')
    user_data = pd.get_dummies(user_data)

    # trying to predict the first row
    data_new = user_data[:1]
    predicted_price = lr.predict(data_new).round(2)

    # Convert predicted price to JSON
    result_data = {'predicted_price': predicted_price[0]}

    # Convert result data to json format
    json_result = json.dumps(result_data)

    server_url = 'http://localhost:3000/predictedPrice'
    
    # Set headers for the request
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to the server
    response = requests.post(server_url, data=json_result, headers=headers)

    # Check response from server
    if response.status_code == 200:
        print('Predicted price successfully sent to the server!')
    else:
        print(f'Failed to send predicted price. Server responded with status code {response.status_code}: {response.text}')


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
        process_json_data(json_data)
        predict()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
