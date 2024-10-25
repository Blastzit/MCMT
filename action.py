import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('keywords.db')

# Open the main.sql file in write mode with utf-8 encoding
with open('keywords.sql', 'w', encoding='utf-8') as f:
    # Use the iterdump method to get the SQL dump
    for line in conn.iterdump():
        f.write('%s\n' % line)

# Close the database connection
conn.close()