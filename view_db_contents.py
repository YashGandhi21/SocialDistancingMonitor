import os
import sqlite3
from datetime import datetime

def store_images(img):
    if not os.path.exists('image_folder'):
        os.makedirs('image_folder')
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H_%M_%S_%f")
        path = "image_folder/{}.jpeg".format(timestampStr)
        img.save(path, 'JPEG')

    else:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H_%M_%S_%f")
        path = "image_folder/{}.jpeg".format(timestampStr)
        img.save(path,'JPEG')

    con = sqlite3.connect("images.db")
    print("Database opened successfully")
    con.execute(
        "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT,Path TEXT NOT NULL)")
    print("Table created successfully")
    con.close()

    try:

        with sqlite3.connect("images.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into images (Path) values (?)", [path])
            con.commit()
            msg = "Image successfully Added"
    except Exception as e:
        print(e)
        con.rollback()
        msg = "We can not add the images to the list"
    finally:
        print(msg)
        con.close()

if __name__ == '__main__':
   # Execute this file to see DB contents
   print("*********************************************************")
   print("printing images.db contents")

   conn = sqlite3.connect('images.db')
   print ("Opened database successfully")

   cursor = conn.execute("SELECT path from images")
   for row in cursor:
      print ("path = ", row[0], "\n")

   print ("Operation done successfully")
   conn.close()

   # For User db
   print("*********************************************************")
   print("printing db.db contents")

   conn = sqlite3.connect('db.db')

   cur = conn.execute("SELECT * FROM User")

   for row in cur:
      print(row)
