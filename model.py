#This is where we will make the model
import requests
import sys
import json
import csv
import math
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def run_test_data(model):
    csv_file_path = "test_output.csv"
    test_csv_file_path = "TestData.csv"
    
    test_data = pd.read_csv("TestData.csv")

    test_data['mainroad'] = test_data['mainroad'].astype('category')
    test_data['guestroom'] = test_data['guestroom'].astype('category')
    test_data['basement'] = test_data['basement'].astype('category')
    test_data['hotwaterheating'] = test_data['hotwaterheating'].astype('category')
    test_data['airconditioning'] = test_data['airconditioning'].astype('category')
    test_data['prefarea'] = test_data['prefarea'].astype('category')
    test_data['furnishingstatus'] = test_data['furnishingstatus'].astype('category')
    test_data = pd.get_dummies(test_data)
            
    x = test_data.drop("id", axis=1)
    
    with open(csv_file_path, 'w', newline="") as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header 
        csv_writer.writerow(['id','price'])

        

        for i in range(len(x)):
            data_new = x[i:i+1]
            prediction = model.predict(data_new).round(2)
            csv_writer.writerow([i, prediction])

        # for row in x:
        #     id_counter += 1
        #     predicted_price = model.predict(row).round(2)
        #     csv_writer.writerow(id_counter, predicted_price)


        # Write the rest of the rows
        # while id_counter < number_of_rows:
            
        #     data_new = x[id_counter:id_counter+1]
        #     print(data_new)
        #     predicted_price = model.predict(data_new).round(2)
        #     csv_writer.writerow([id_counter+1, predicted_price])
        #     id_counter += 1

def evaluate_model(x_test, y_test, model):
    # Evaluate models performance before remvoing outliers
    print("test score:" + str(model.score(x_test, y_test).round(3)))

    # Mean squared error
    y_pred = model.predict(x_test)
    print("Mean Squared error:" + str(math.sqrt(mean_squared_error(y_test, y_pred))))

    # Calculate permutation importance
    perm_importance = permutation_importance(model, x_test, y_test, metric=mean_squared_error)

    # Sort features by importance score
    sorted_importance = sorted(perm_importance.items(), key=lambda x: x[1], reverse=True)

    # Print feature importance scores
    print("\nPermutation Importance:")
    for feature, importance in sorted_importance:
        print(f"{feature}: {importance}")

def create_linear_regression_model(training_data):
    
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
    evaluate_model(x_test, y_test, lr)
    
    return lr

def removeOutliers(df):
    # Assuming 'value' is the column with numeric values
    z_scores = stats.zscore(df['area'])
    threshold = 3
    outlier_indices = (abs(z_scores) > threshold)

    # Step 3: Filter or remove the outliers from the DataFrame
    df_no_outliers = df[~outlier_indices]

    # Step 4: Write the filtered DataFrame back to a CSV file
    df_no_outliers.to_csv('filtered_file.csv', index=False)

def permutation_importance(model, X, y, metric, random_state=42):
    baseline = metric(y, model.predict(X))
    importance_scores = {}
    np.random.seed(random_state)
    for feature in X.columns:
        X_permuted = X.copy()
        X_permuted[feature] = np.random.permutation(X_permuted[feature])
        permuted_score = metric(y, model.predict(X_permuted))
        importance_scores[feature] = baseline - permuted_score
    return importance_scores


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

    lr = create_linear_regression_model(training_data)
    removeOutliers(training_data)
    cleaned_data = pd.read_csv("filtered_file.csv")
    lr_no_outliers = create_linear_regression_model(cleaned_data)

    run_test_data(lr_no_outliers)
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
    predicted_price = lr_no_outliers.predict(data_new).round(2)

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
