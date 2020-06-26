import sqlite3

conn = sqlite3.connect('images.db')
print ("Opened database successfully")

cursor = conn.execute("SELECT path from images")
for row in cursor:
   print ("path = ", row[0], "\n")

print ("Operation done successfully")
conn.close()