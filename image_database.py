import os
import sqlite3
from datetime import datetime

def store_images(img):
    if not os.path.exists('image_folder'):
        os.makedirs('image_folder')
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H_%M_%S_%f")
        path = "image_folder/{}.jpg".format(timestampStr)
        img.save(path, 'JPEG')

    else:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H_%M_%S_%f")
        path = "image_folder/{}.jpg".format(timestampStr)
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
