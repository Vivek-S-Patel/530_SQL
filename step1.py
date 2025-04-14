import sqlite3
import pandas as pd

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect("spreadsheet.db")
cursor = conn.cursor()

# Load CSV into DataFrame
csv_file = input("Enter CSV file name (e.g., data.csv): ")
df = pd.read_csv(csv_file)

# Create a table based on the CSV data
df.to_sql("my_table", conn, if_exists="replace", index=False)

# Confirm that the table has been created
print(f"CSV data from '{csv_file}' loaded into the table 'my_table'.")

# Close the database connection
conn.close()
