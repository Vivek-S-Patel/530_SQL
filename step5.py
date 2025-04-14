import sqlite3
import openai

# Connect to SQLite database
conn = sqlite3.connect("spreadsheet.db")
cursor = conn.cursor()

# OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

# Simple function to generate SQL using OpenAI
def generate_sql(table_name, query):
    prompt = f"Table: {table_name}. Write a SQL query for: {query}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Main loop
while True:
    table_name = input("Table name (or 'exit' to quit): ").strip()
    if table_name.lower() == 'exit':
        break
    
    query = input("Your query: ").strip()

    # Generate and run SQL
    sql_query = generate_sql(table_name, query)
    print("Generated SQL:", sql_query)
    
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    print("Results:", results)

# Close connection
conn.close()
