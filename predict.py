import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data from the CSV file
csv_file = "historical_metrics.csv"
data = pd.read_csv(csv_file)

# Ensure data has the expected structure
required_columns = ["Month", "Sales Person", "Total Actions", "Total Clients", "total_reservations", "Avg Actions per Client"]
if not all(col in data.columns for col in required_columns):
    raise ValueError("CSV file is missing required columns.")

# Convert 'Month' to datetime and sort values
data['Month'] = pd.to_datetime(data['Month'], format='%Y-%m-%d')
data = data.sort_values(by=['Sales Person', 'Month'])

# Handle missing values by filling them with the column mean
data['Total Actions'] = data['Total Actions'].fillna(data['Total Actions'].mean())
data['Total Clients'] = data['Total Clients'].fillna(data['Total Clients'].mean())
data['total_reservations'] = data['total_reservations'].fillna(data['total_reservations'].mean())
data['Avg Actions per Client'] = data['Avg Actions per Client'].fillna(data['Avg Actions per Client'].mean())

# Create a list to store predictions as dictionaries (for later conversion to DataFrame)
predictions_list = []

# Group data by each salesperson and train a model
for salesperson, group in data.groupby('Sales Person'):
    # Ensure the data is in chronological order
    group = group.sort_values(by='Month')

    # Encode month as an integer (to use as the feature)
    group['Month_Num'] = np.arange(len(group))

    # Separate the features (Month_Num) and targets
    X = group[['Month_Num']]
    y_total_actions = group['Total Actions']
    y_total_clients = group['Total Clients']
    y_total_reservations = group['total_reservations']
    y_avg_actions_per_client = group['Avg Actions per Client']

    # Train a separate model for each metric
    model_actions = LinearRegression()
    model_clients = LinearRegression()
    model_reservations = LinearRegression()
    model_avg_actions = LinearRegression()

    # Fit the models
    model_actions.fit(X, y_total_actions)
    model_clients.fit(X, y_total_clients)
    model_reservations.fit(X, y_total_reservations)
    model_avg_actions.fit(X, y_avg_actions_per_client)

    # Predict for the next month (using a DataFrame with the same column name)
    next_month_num = pd.DataFrame([[X['Month_Num'].max() + 1]], columns=['Month_Num'])
    predicted_total_actions = model_actions.predict(next_month_num)[0]
    predicted_total_clients = model_clients.predict(next_month_num)[0]
    predicted_total_reservations = model_reservations.predict(next_month_num)[0]
    predicted_avg_actions_per_client = model_avg_actions.predict(next_month_num)[0]

    # Append the prediction as a dictionary to the list
    predictions_list.append({
        "Sales Person": salesperson,
        "Predicted Total Actions": predicted_total_actions,
        "Predicted Total Clients": predicted_total_clients,
        "Predicted Total Reservations": predicted_total_reservations,
        "Predicted Avg Actions per Client": predicted_avg_actions_per_client
    })

# Convert the predictions list to a DataFrame and save it to a new CSV file
predictions = pd.DataFrame(predictions_list)
predictions.to_csv("predicted_next_month.csv", index=False)
print("Predictions saved to 'predicted_next_month.csv'")
