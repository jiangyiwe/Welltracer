from  app import db, create_app, WatchHistory

# 创建一个Flask应用实例
'''
app = create_app()

# 激活上下文
with app.app_context():
    # 创建一个新的观看记录实例
    new_record = WatchHistory(user_id='3', video_class='tricep Pushdown')

    # 添加记录到会话并提交到数据库
    db.session.add(new_record)
    db.session.commit()

import requests
import base64

# Open the image, convert it to base64
image_path = r'C:\Users\Jiang\flask-vue-crud\data\b75f5913-ca28-41a7-b985-30ab40045d7a.webp'
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Replace these with the actual data you want to send
data = {
    'class_override': 'Bread',  # or whatever class you want to override with
    'calories_override': '250',  # or your own value
    'kj_override': '1046',  # or your own value
    'mass': '100',  # or your own value
    'img_str': encoded_string  # the base64 encoded image string
}

# The URL to your `/confirm_prediction` route
url = 'http://127.0.0.1:5001/confirm_prediction'

# Sending post request to the url with the data
response = requests.post(url, data=data)

# Printing the response text
print(response.text)

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('predictions.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Drop the table
cursor.execute("DROP TABLE IF EXISTS predictions")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
'''