import sqlite3

import sqlite3

conn = sqlite3.connect('main.db')
cursor = conn.cursor()

cursor.execute("""
    UPDATE degree_group
    SET group_name = 'modules'
    WHERE group_name = 'group_year1'
""")

conn.commit()
conn.close()