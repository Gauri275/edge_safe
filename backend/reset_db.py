import os
import sqlite3

db_path = 'emergency.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('DROP TABLE IF EXISTS first_aid')
    conn.execute('DROP TABLE IF EXISTS shelters')
    conn.execute('DROP TABLE IF EXISTS evacuation_routes')
    conn.commit()
    conn.close()
    print("All tables dropped.")

print("Now run: python db_seed.py")