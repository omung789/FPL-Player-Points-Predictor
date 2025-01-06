# Importing packages
import numpy as np
import pandas as pd
import random
import os
import seaborn as sns

import matplotlib.pyplot as plt

from scipy import optimize
from sklearn import datasets as skdataset
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from pathlib import Path

from sklearn.decomposition import PCA

columns_to_drop = ['name', 'team']

#stats that are not available before the gameweek - i.e. cant look at goals scored as match hasnt been played yet
columns_to_drop.extend(['influence', 'red_cards', 'transfers_out', 'minutes', 'result', 'selected', 'goals scored (team)', 'total_points', 'transfers_balance', 'penalties_missed', 'goals_conceded', 'own_goals', 'saves', 'creativity', 'transfers_in', 'penalties_saved', 'bps', 'assists', 'goals_scored', 'bonus', 'ict_index', 'clean_sheets', 'goals conceded (team)', 'yellow_cards', 'threat'])

from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{str(current_year)}-{str(current_year + 1)[2:]}"

current_path = os.getcwd()
data_directory = os.path.join(current_path, "data")
#get data from previous seasons
train = pd.read_csv(os.path.join(data_directory, "combined_previous_seasons_data.csv"), index_col=0)

old_gameweek_cleaned = []
#get data from previous gameweeks in the current season
gameweek = 29
for i in range(1, gameweek):
    file_path = os.path.join(data_directory,year,"results",f"gameweek_{i}_results.csv")
    old_gameweek_cleaned.append(pd.read_csv(file_path))

old_gameweeks = pd.concat(old_gameweek_cleaned)[train.columns]

train = pd.concat([train, old_gameweeks])
categorical_columns = [col for col in train.columns if train[col].dtype == 'object']

# Convert categorical columns to numerical using LabelEncoder
label_encoders = {}
for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    if col not in columns_to_drop:
        train[col + '_Numerical'] = label_encoders[col].fit_transform(train[col])
        train.drop(columns=col, inplace=True)

gameweek = 31
# data for current gameweek we want to predict on
test_file_path = os.path.join(data_directory, year, "fixtures",f"gameweek_{gameweek}_fixtures.csv")
test = pd.read_csv(test_file_path, index_col=0)

# make directory to store results
os.makedirs(f"{current_path}/data/{year}/machine learning", exist_ok=True)

target = train['total_points']
train.drop(columns=columns_to_drop, inplace=True)
correlation = train.corr()

threshold = 0.7

high_correlation_features = set()
high_correlation_pairs = set()
for i in range(len(correlation.columns)):
    for j in range(i+1, len(correlation.columns)):
        if abs(correlation.iloc[i, j]) > threshold:
            # Add the pair of indexes to the set
            high_correlation_features.add(correlation.columns[i])
            high_correlation_features.add(correlation.columns[j])
            high_correlation_pairs.add((correlation.columns[i], correlation.columns[j]))

# print("Unique pairs of indexes with high correlation:", high_correlation_pairs)
print("\nFeatures with high correlation:", high_correlation_features)

# plt.figure(figsize=(20, 20))
# sns.heatmap(correlation, annot=True, cmap='coolwarm')
# plt.title('Correlation Matrix')
# plt.show()

# # Create a new correlation matrix for high correlation features
# correlation_high = correlation.loc[list(high_correlation_features), list(high_correlation_features)]

# plt.figure(figsize=(10, 10))
# heatmap = sns.heatmap(correlation_high, annot=True, cmap='coolwarm')  # Adjust size as needed
# heatmap.set_title('Correlation Matrix for High Correlation Features', fontsize=24)  # Adjust size as needed
# plt.xticks(fontsize=14)  # Adjust size of x-axis ticks (feature names)
# plt.yticks(fontsize=14, rotation=0)  # Adjust size of y-axis ticks (feature names)
# plt.tight_layout()
# plt.show()

# Drop features that are highly correlated with lots of other features
high_correlation_features_new = ['influence_mean_last_3_gw', 'goals_conceded_mean_last_3_gw', 'creativity_mean_last_3_gw', 'threat_mean_last_3_gw', 'goals scored (team)_mean_last_3_gw', 'bonus_mean_last_3_gw']
train.drop(columns=high_correlation_features_new, inplace=True)

data = train.copy()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred_train = regressor.predict(X_train)
y_pred_test = regressor.predict(X_test)

from sklearn.linear_model import Ridge

ridge_regressor = Ridge(alpha=1.0) 

ridge_regressor.fit(X_train, y_train)

y_pred_train_ridge = ridge_regressor.predict(X_train)
y_pred_test_ridge = ridge_regressor.predict(X_test)

train_mse = mean_squared_error(y_train, y_pred_train)
test_mse = mean_squared_error(y_test, y_pred_test)

train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)

print("Train MSE:", train_mse)
print("Test MSE:", test_mse)

print("Train MAE:", train_mae)
print("Test MAE:", test_mae)

train_mse_ridge = mean_squared_error(y_train, y_pred_train_ridge)
test_mse_ridge = mean_squared_error(y_test, y_pred_test_ridge)

train_mae_ridge = mean_absolute_error(y_train, y_pred_train_ridge)
test_mae_ridge = mean_absolute_error(y_test, y_pred_test_ridge)

print("Ridge Regression Train MSE:", train_mse_ridge)
print("Ridge Regression Test MSE:", test_mse_ridge)

print("Ridge Regression Train MAE:", train_mae_ridge)
print("Ridge Regression Test MAE:", test_mae_ridge)

assert 1 == 0

names = test['name']
positions = test['position']
teams = test['team']
price = test['value']
# set mintues to positive value so best team algorithm thinks everyone will play
minutes = [1 for _ in range(len(names))]

test.drop(columns=['name','team'], inplace=True)
test.drop(columns=high_correlation_features_new, inplace=True)

for col, encoder in label_encoders.items():
    if col not in columns_to_drop:
        test[col + '_Numerical'] = encoder.transform(test[col])
        test.drop(columns=col, inplace=True)

linear_regression_predictions = regressor.predict(test)
ridge_regression_predictions = ridge_regressor.predict(test)

predictions = pd.DataFrame({'PLAYER': names, 'TEAM': teams, 'POSITION': positions, 'PRICE': price, 'MINUTES': minutes, 'Linear Regression POINTS Predictions': linear_regression_predictions})
predictions.to_csv(f"{current_path}/data/{year}/machine learning/gameweek_{gameweek}_predictions.csv")