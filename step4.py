import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("spreadsheet.db")
cursor = conn.cursor()

print("Commands: load, tables, query, exit")

while True:
    cmd = input("Enter command: ").strip().lower()

    if cmd == "load":
        file = input("CSV file name (like data.csv): ")
        table = input("Table name to use: ")
        try:
            df = pd.read_csv(file)
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"Loaded '{file}' into table '{table}'\n")
        except Exception as e:
            print("Error loading file:", e)

    elif cmd == "tables":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor.fetchall():
            print("Table:", row[0])
        print()

    elif cmd == "query":
        sql = input("Type your SQL query:\n")
        try:
            cursor.execute(sql)
            for row in cursor.fetchall():
                print(row)
            print()
        except Exception as e:
            print("Error:", e)

    elif cmd == "exit":
        print("Bye!")
        break

    else:
        print("Unknown command. Try again.")

# Close database connection
conn.close()
