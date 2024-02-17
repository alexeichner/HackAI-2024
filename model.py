#This is where we will make the model
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math

data = pd.read_csv("HousingDataset.csv")

#Converting object types to category types
data['mainroad'] = data['mainroad'].astype('category')
data['guestroom'] = data['guestroom'].astype('category')
data['basement'] = data['basement'].astype('category')
data['hotwaterheating'] = data['hotwaterheating'].astype('category')
data['airconditioning'] = data['airconditioning'].astype('category')
data['prefarea'] = data['prefarea'].astype('category')
data['furnishingstatus'] = data['furnishingstatus'].astype('category')

#Creating some dataplots for housing data
sns.set_style("whitegrid")
sns.pairplot(
    data[['price', 'area', 'furnishingstatus']],
    hue = 'furnishingstatus',
    height = 5,
    palette = "Set1")
#plt.show()

#Do one-hot encoding
data = pd.get_dummies(data)
#This line shows how each categorical data column is now converted to something that can be represented with numbers
# print(data.columns)

# Start building a regression model

# Target variable (What we want to predict)
y = data["price"]

# Drop the target variable
x = data.drop("price", axis=1)

# 80/20 split between training and testing
x_train,x_test,y_train,y_test = train_test_split(
    x,y,
    train_size = 0.80,
    random_state = 1)

# Create an instance of the linear regression model
lr = LinearRegression()

# Build using the training data
lr.fit(x_train, y_train)

# Model Evaluation

print("test score:" + str(lr.score(x_test, y_test).round(3)))
print("train score:" + str(lr.score(x_train, y_train).round(3)))

# Mean squared error
y_pred = lr.predict(x_test)
print("Mean Squared error:" + str(math.sqrt(mean_squared_error(y_test, y_pred))))

# Model prediction

# trying to predict the first row
data_new = x_train[:1]

print("Predicted price:" + str(lr.predict(data_new).round(2)))
print("Real Value:" + str(y_train[:1]))


