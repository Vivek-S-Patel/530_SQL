import pandas as pd
import sqlite3

# Load CSV into DataFrame
df = pd.read_csv('example_data.csv')

# Function to map pandas dtypes to SQLite types
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    else:
        return "TEXT"

# Function to generate CREATE TABLE SQL dynamically
def generate_create_table_sql(table_name, dataframe):
    columns = dataframe.columns
    dtypes = dataframe.dtypes
    sql_columns = []

    for col, dtype in zip(columns, dtypes):
        sql_type = map_dtype(dtype)
        sql_columns.append(f'"{col}" {sql_type}')
    
    columns_sql = ", ".join(sql_columns)
    create_stmt = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});'
    return create_stmt

# Create table using generated SQL
conn = sqlite3.connect('spreadsheet.db')
cursor = conn.cursor()

table_name = 'dynamic_table'
create_table_sql = generate_create_table_sql(table_name, df)
print("Executing SQL:\n", create_table_sql)
cursor.execute(create_table_sql)

# Insert data
df.to_sql(table_name, conn, if_exists='append', index=False)
print(f"Data inserted into '{table_name}'.")

conn.commit()
conn.close()
