import pandas as pd
import numpy as np


# Ignoring Warning
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split

import sklearn.metrics as sm



df = pd.read_csv('Dataset1.csv')

print(f"Number of rows and columns in the Dataset : {df.shape}")
print()

# This provides the all the columns present in the dataset
print(f"The columns present in the dataset : {df.shape}")
print()

# This provides the first 5 obeservations(rows) of the dataset
print(f"Head of the dataset {df.head()}")
print()

# This provides a breif description of the Dataset
print(f"Description of the Dataset : {df.describe()}")
print()


# This gives the correaltion of between each column in the data set
print(f"Correaltion : {df.corr()}")
print()

# If there are any duplicate values, it should be dropped
df = df.drop_duplicates()
print(f"Checking the shape of the Dataset (After dropping duplicate Values) : {df.shape}")
print()

# Check if there are any null values
print(f"Null Values if Present : {df.isnull().sum()}")
print()

# If there are any null values they should be dropped
df = df.dropna()
print(f"Null Values : {df.isnull().sum()}")
print()


y = df.AQI
X = df.drop('AQI', axis = 1)


# Split X and y into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Print the number of observation in X_train, X_test, y_train and y_test
print(f"Number of observations in X_train : {X_train.shape}")
print()

print(f"Number of observations in X_test : {X_test.shape}")
print()

print(f"Number of observations in y_train : {y_train}")
print()

print(f"Number of observations in y_test : {y_test}")
print()



from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

model_1 = RandomForestRegressor()
model_2 = LinearRegression()

model_1.fit(X_train, y_train)
model_2.fit(X_train, y_train)


# Predict Test set Results
y_pred1 = model_1.predict(X_test)
y_pred2 = model_2.predict(X_test)

df1 = pd.DataFrame({'Actual' : y_test, 'Predicted' : y_pred1})
print(df1)
print()

y_pred1 = np.array(y_pred1).reshape(-1, 1)

accuracy = sm.r2_score(y_test, y_pred1)

print(f"Accuracy of Random Forest Regressor :  {accuracy * 100}")
print()

accuracy = sm.r2_score(y_test, y_pred2)

print(f"Accuracy of Linear Regression :  {accuracy * 100}")
print()

# from import joblib
import joblib

# Save the model as a Pickle in a File
joblib.dump(model_1, "final_pickle_model.pkl")

# Load the model from the file
final_model = joblib.load("final_pickle_model.pkl")

pred = final_model.predict(X_test)

accuracy = sm.r2_score(y_test,pred)

print(f"Accuracy of the Final Model is : {accuracy * 100}%")
