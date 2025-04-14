import pandas as pd
import sqlite3
import datetime

# Simple error logging
def log_error(message):
    with open("error_log.txt", "a") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{time}] {message}\n")

# Ask the user what to do on conflict
def ask_user():
    print("Table already exists and has a different structure.")
    print("What would you like to do?")
    print("  [O] Overwrite the table")
    print("  [R] Rename the new table")
    print("  [S] Skip adding this data")
    choice = input("Enter your choice (O/R/S): ").strip().lower()
    return choice

# Main function
def load_csv(csv_file, table_name):
    try:
        # Load CSV into a DataFrame
        df = pd.read_csv(csv_file)

        # Connect to SQLite
        conn = sqlite3.connect("spreadsheet.db")
        cursor = conn.cursor()

        # Check if table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        exists = cursor.fetchone()

        if exists:
            # Get existing columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            existing_cols = [row[1] for row in cursor.fetchall()]
            new_cols = df.columns.tolist()

            if set(existing_cols) != set(new_cols):
                choice = ask_user()

                if choice == 'o':
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                    print(f"Table '{table_name}' has been overwritten.")

                elif choice == 'r':
                    new_name = input("Enter new table name: ").strip()
                    df.to_sql(new_name, conn, if_exists="replace", index=False)
                    print(f"New table '{new_name}' has been created.")

                elif choice == 's':
                    print("Skipping this file.")
                else:
                    print("Invalid choice. Skipping.")
                    log_error("Invalid input during schema conflict.")
            else:
                df.to_sql(table_name, conn, if_exists="append", index=False)
                print(f"Data added to existing table '{table_name}'.")

        else:
            # If table doesn't exist, just create it
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Table '{table_name}' created and data added.")

        conn.commit()
        conn.close()

    except Exception as e:
        print("Something went wrong. Check error_log.txt for details.")
        log_error(str(e))

# Example usage
load_csv("example_data.csv", "my_table")
