import requests
import csv

# Define the API endpoint
api_url = "https://alex-academy.net/alexa/alex_system/API/general_report.php"

# Define the output CSV file name
csv_file = "historical_metrics.csv"

try:
    # Make a request to the API
    response = requests.get(api_url)
    response.raise_for_status()  # Check for HTTP request errors

    # Parse the JSON response
    data = response.json()

    # Check if the response has the expected structure
    if 'employee_performance' not in data:
        raise ValueError("Unexpected response structure. 'employee_performance' key not found.")

    # Prepare to write data to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the headers (you can adjust these based on the exact structure of the response)
        headers = ["Month", "Sales Person", "Total Actions", "Total Clients", "total_reservations", "Avg Actions per Client"]
        writer.writerow(headers)

        # Write data rows
        for month, metrics in data['employee_performance'].items():
            for metric in metrics:
                # Replace with actual metric keys if needed
                sales_person = metric.get("sales_person")
                total_actions = metric.get("total_actions")
                total_clients = metric.get("total_clients")
                total_reservations = metric.get("total_reservations")
                avg_actions_per_client = metric.get("avg_actions_per_client")

                # Write row for each employee's performance
                writer.writerow([month, sales_person, total_actions, total_clients, total_reservations, avg_actions_per_client])

    print(f"Data successfully written to {csv_file}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except ValueError as ve:
    print(f"Data error: {ve}")
except Exception as e:
    print(f"An error occurred: {e}")
