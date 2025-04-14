import pandas as pd
import sqlite3
import os


# Manually create a table in SQLite.
csv_filename = 'example_data.csv'

# Only create the CSV if it doesn't already exist
if not os.path.exists(csv_filename):
    csv_data = {
        'Column1': [1, 2, 3],
        'Column2': [10, 20, 30],
        'Column3': ['A', 'B', 'C']
    }
    df_initial = pd.DataFrame(csv_data)
    df_initial.to_csv(csv_filename, index=False)
    print(f"Created CSV: {csv_filename}")
else:
    print(f"CSV already exists: {csv_filename}")


# Load CSV to dataframe

df = pd.read_csv(csv_filename)
print("\nLoaded DataFrame:")
print(df)


# Insert into SQLITE DB
conn = sqlite3.connect('spreadsheet.db')
cursor = conn.cursor()

# Check if the table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sheet_data'")
table_exists = cursor.fetchone()

if table_exists:
    # Get existing columns
    cursor.execute("PRAGMA table_info(sheet_data)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    # Add any missing columns
    for col in df.columns:
        if col not in existing_columns:
            cursor.execute(f"ALTER TABLE sheet_data ADD COLUMN {col} TEXT")
    
    # Append data
    df.to_sql('sheet_data', conn, if_exists='append', index=False)
    print("\nAppended data to existing table with schema handling.")
else:
    # Create new table and insert data
    df.to_sql('sheet_data', conn, if_exists='replace', index=False)
    print("\nCreated new table and inserted data.")

conn.commit()

# Run Examples
print("\nAll Data:")
for row in conn.execute("SELECT * FROM sheet_data"):
    print(row)

print("\nRows where Column2 > 15:")
for row in conn.execute("SELECT * FROM sheet_data WHERE Column2 > 15"):
    print(row)

print("\nFirst 2 Rows:")
for row in conn.execute("SELECT * FROM sheet_data LIMIT 2"):
    print(row)

print("\nSelected Columns (Column1, Column3):")
for row in conn.execute("SELECT Column1, Column3 FROM sheet_data"):
    print(row)

conn.close()
