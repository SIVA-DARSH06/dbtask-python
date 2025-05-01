import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Connect to SQLite database (create if it doesn't exist)
db_file = "sales_data.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 2: Create table and insert sample data (run only if DB is empty)
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
''')

# Insert data only if table is empty
cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Apple", 10, 0.5),
        ("Bananas", 15, 0.3),
        ("Apples", 20, 0.5),
        ("Oranges", 5, 0.8),
        ("Bananas", 10, 0.3),
        ("Oranges", 10, 0.8)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()

# Step 3: Run SQL query
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue 
FROM sales 
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# Step 4: Print the result
print("Sales Summary:")
print(df)

# Step 5: Plot bar chart
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()

# Step 6: Save and show plot
plt.savefig("sales_chart.png")
plt.show()

# Close the connection
conn.close()
