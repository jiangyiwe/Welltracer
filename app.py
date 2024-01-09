import requests
from flask import *
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import pandas as pd
# Other necessary imports and model definition code goes here、
import re
import os
import io  # Added import for io
import base64
# Other functions or code related to your model can go here
import random
from flask_sqlalchemy import SQLAlchemy
import requests
from google.cloud import vision
from google.oauth2 import service_account
# allow CORS
from flask_cors import CORS
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
# 定义一个路由暴露给网站的访问接口
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watch_history.db'
    db.init_app(app)


    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        db.create_all()  # 在应用上下文中创建数据库表
    scheduler = BackgroundScheduler()
    model = load_model("./model-re-image.h5")
    model_sport = load_model("./sport_model.h5")
    classes_sport = sorted(os.listdir("./data/sport"))
    model = load_model("./model-re-image.h5")

    model_sport = load_model("./sport_model.h5")

    classes_sport = sorted(os.listdir("./data/sport/"))
    model_calories=load_model('./data/food-101/final_model.hdf5')

    credentials = service_account.Credentials.from_service_account_file("data/recotexte-409521-6e14f0a168bc.json")
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # 读取CSV文件并创建食物名称到卡路里和千焦的映射
    calories_df = pd.read_csv('./data/calories.csv')
    calories_dict = pd.Series(calories_df.Cals_per100grams.values, index=calories_df.FoodItem).to_dict()
    kj_dict = pd.Series(calories_df.KJ_per100grams.values, index=calories_df.FoodItem).to_dict()


    # Assuming you have the following labels from your training
    labels = {
        0: 'Bread',
        1: 'Dairy product',
        2: 'Dessert',
        3: 'Egg',
        4: 'Fried food',
        5: 'Meat',
        6: 'Noodles-Pasta',
        7: 'Rice',
        8: 'Seafood',
        9: 'Soup',
        10: 'Vegetable-Fruit'
    }

    # 定义食品名称格式转换函数
    def format_food_name(name):
        return name.replace("_", " ").title()

    @app.route('/')
    def hello_world():
        return 'Hello World'

    @app.route('/classes', methods=['GET'])
    def list_classes():
        return jsonify(classes_sport)

    @app.route('/random_videos', methods=['GET'])
    def random_videos():
        num_videos = 5  # The number of videos you want to return

        video_selections = []
        for _ in range(num_videos):
            video_class = random.choice(classes_sport)
            video_path = os.path.join("data/sport", video_class)
            video_files = os.listdir(video_path)
            video_file = random.choice(video_files)

            # Here we are creating a URL path for the video
            video_url = f"/video/{video_class}/{video_file}"  # This will be used to create a link to the actual video

            video_info = {
                'class': video_class,
                'filename': video_file,
                'url': video_url  # The URL where the video can be accessed
            }
            video_selections.append(video_info)

        return jsonify(video_selections)

    @app.route('/video/<video_class>/<video_filename>', methods=['GET'])
    def serve_video(video_class, video_filename):
        video_path = os.path.join("data/sport", video_class, video_filename)
        return send_file(video_path, mimetype='video/mp4')  # Ensure the mimetype matches your video format

    # 新增一个路由来记录观看
    @app.route('/record_watch', methods=['POST'])
    def record_watch():
        data = request.get_json()
        print(f"Received data: {data}")  # 添加日志打印

        user_id = data.get('user_id')
        video_class = data.get('video_class')

        # 检查 user_id 和 video_class 是否存在
        if not user_id or not video_class:
            return jsonify({"error": "Missing user_id or video_class in request"}), 400

        # 创建新的观看历史记录并保存到数据库
        new_watch_history = WatchHistory(user_id=user_id, video_class=video_class)
        db.session.add(new_watch_history)
        db.session.commit()

        return jsonify({"status": "success", "message": "Recorded video watch successfully"})


    @app.route('/history', methods=['GET'])
    def view_history():
        # 查询数据库获取所有观看记录
        history_records = WatchHistory.query.all()

        # 将每条记录转换为字典格式
        history_list = []
        for record in history_records:
            history_list.append({
                "id": record.id,
                "user_id": record.user_id,
                "video_class": record.video_class
            })

        # 返回JSON格式的响应
        return jsonify(history_list)

    @app.route('/recommend', methods=['GET'])
    def recommend_videos():
        user_id = request.args.get('user_id')  # 假设用户ID通过查询参数传递

        # 从数据库获取该用户的所有观看记录
        user_watches = WatchHistory.query.filter_by(user_id=user_id).all()

        # 如果找不到用户或用户没有观看历史
        if not user_watches:
            return jsonify({"error": "No history found for the user"}), 404

        # 获取用户观看过的所有视频类别
        watched_classes = set(record.video_class for record in user_watches)

        # 存储所有视频的列表
        all_videos_list = []

        # 收集每个类别下的所有视频
        for video_class in watched_classes:
            video_path = os.path.join("./data/sport", video_class)
            try:
                all_videos = os.listdir(video_path)
                all_videos_list.extend([(video_class, video) for video in all_videos])
            except FileNotFoundError:
                continue  # 如果找不到该类别的目录，跳过该类别

        # 从所有视频中随机选择5个进行推荐
        num_recommendations = min(5, len(all_videos_list))
        recommendations = random.sample(all_videos_list, num_recommendations)

        # 构建推荐视频的信息列表
        all_recommendations_info = [{
            "class": video_class,
            "filename": video,
            "url": f"/video/{video_class}/{video}"
        } for video_class, video in recommendations]

        return jsonify(all_recommendations_info)


    # 假设train_data_dir是你的训练数据目录
    train_data_dir = r'C:\Users\Jiang\flask-vue-crud\data\food-101\train'

    # 使用ImageDataGenerator创建一个生成器
    train_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(224, 224),
        batch_size=16,
        class_mode='categorical')

    def init_db():
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS predictions 
                     (date text, predicted_class text, mass real, calories real, kj real, image BLOB)''')
        conn.commit()
        conn.close()

    init_db()

    def clear_predictions():
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        # Delete all records from the table
        c.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()

    # Clear the predictions table
    #clear_predictions()

    @app.route('/predict_img', methods=['GET'])
    def form():
        # HTML form to submit weight and image
        return '''
            <form method="post" enctype="multipart/form-data">
                Mass in grams: <input type="number" name="mass"><br>
                Image: <input type="file" name="image"><br>
                <input type="submit" value="Predict">
            </form>
        '''

    # 从生成器获取食品列表
    food_list = list(train_generator.class_indices.keys())

    @app.route('/predict_img', methods=['POST'])
    def predict_img():
        mass = float(request.form.get('mass', 100))
        image_file = request.files['image']
        if not image_file:
            return "No image provided."

        # Open and process the image file
        img = Image.open(image_file.stream).resize((256, 256))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict the class using your model
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)
        predicted_class_name = labels[predicted_class_index[0]]

        # Predict calories using your model
        pred_calories = model_calories.predict(img_array)
        index = np.argmax(pred_calories)
        formatted_name = format_food_name(food_list[index])
        calories_per100g = calories_dict.get(formatted_name, "Unknown")
        kj_per100g = kj_dict.get(formatted_name, "Unknown")

        # Calculate the actual calories and kj based on the mass
        if calories_per100g != "Unknown":
            try:
                calories_per100g = float(calories_per100g.replace(' cal', ''))
                actual_calories = f"{calories_per100g * mass / 100:.2f}"
            except ValueError:
                actual_calories = "Unknown"
        else:
            actual_calories = "Unknown"

        if kj_per100g != "Unknown":
            try:
                kj_per100g = float(kj_per100g.replace(' kJ', ''))
                actual_kj = f"{kj_per100g * mass / 100:.2f}"
            except ValueError:
                actual_kj = "Unknown"
        else:
            actual_kj = "Unknown"

        # Convert the image to a format that can be displayed in HTML
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # If unknown values, prompt user to input the values
        if calories_per100g == "Unknown" or kj_per100g == "Unknown":
            return render_template_string('''
                <html>
                    <body>
                        <h2>Predicted Class: {{ predicted_class_name }}</h2>
                        <img src='data:image/jpeg;base64,{{ img_str }}'/>
                        <form action="/confirm_prediction" method="post">
                            <p>If the predicted class is incorrect, select the correct one:</p>
                            <select name="class_override">
                                {% for label in labels.values() %}
                                <option value="{{ label }}" {% if label == predicted_class_name %}selected{% endif %}>{{ label }}</option>
                                {% endfor %}
                            </select><br>
                            <p>Enter the calories per 100g (leave blank if unknown):</p>
                            <input type="text" name="calories_override"><br>
                            <p>Enter the energy in kJ per 100g (leave blank if unknown):</p>
                            <input type="text" name="kj_override"><br>
                            <input type="hidden" name="mass" value="{{ mass }}">
                            <input type="hidden" name="img_str" value="{{ img_str }}">
                            <input type="submit" value="Confirm">
                        </form>
                    </body>
                </html>
            ''', predicted_class_name=predicted_class_name, labels=labels, img_str=img_str, mass=mass)

        # Otherwise, continue with processing
        # Connect to the database and insert the data
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions (date, predicted_class, mass, calories, kj, image) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now(), predicted_class_name, mass, actual_calories, actual_kj, img_str))
        conn.commit()
        conn.close()

        # Create an HTML response
        html = f"<html><body>"
        html += f"<h2>Predicted Class: {predicted_class_name}</h2>"
        html += f"<p>Calories for {mass}g: {actual_calories} cal</p>"
        html += f"<p>Energy for {mass}g: {actual_kj} kJ</p>"
        html += f"<img src='data:image/jpeg;base64,{img_str}'/>"
        html += f"<br><br><a href='/predict_img'>Make another prediction</a>"
        html += "</body></html>"

        return html

    @app.route('/confirm_prediction', methods=['POST'])
    def confirm_prediction():
        class_override = request.form.get('class_override')
        calories_override = request.form.get('calories_override', "Unknown")
        kj_override = request.form.get('kj_override', "Unknown")
        mass = float(request.form.get('mass'))
        img_str = request.form.get('img_str')

        predicted_class_name = class_override if class_override else "Unknown"

        # Calculate the actual calories and kj based on the mass
        if calories_override != "Unknown":
            try:
                calories_per100g = float(calories_override.replace(' cal', ''))
                actual_calories = f"{calories_per100g * mass / 100:.2f}"
            except ValueError:
                actual_calories = "Unknown"
        else:
            actual_calories = "Unknown"

        if kj_override != "Unknown":
            try:
                kj_per100g = float(kj_override.replace(' kJ', ''))
                actual_kj = f"{kj_per100g * mass / 100:.2f}"
            except ValueError:
                actual_kj = "Unknown"
        else:
            actual_kj = "Unknown"

        # Insert the confirmed data into database
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions (date, predicted_class, mass, calories, kj, image) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now(), predicted_class_name, mass, actual_calories, actual_kj, img_str))
        conn.commit()
        conn.close()

        # Create an HTML response with confirmed data
        return render_template_string('''
               <html>
                   <body>
                       <h2>Edit and Confirm Your Data</h2>
                       <form action="/update_prediction" method="post">  <!-- Notice the action points to a new route for updating -->
                           <label>Class:</label>
                           <input type="text" name="class_override" value="{{ predicted_class_name }}"><br>
                           <label>Calories per 100g:</label>
                           <input type="text" name="calories_override" value="{{ actual_calories }}"><br>
                           <label>Energy in kJ per 100g:</label>
                           <input type="text" name="kj_override" value="{{ actual_kj }}"><br>
                           <label>Mass in grams:</label>
                           <input type="text" name="mass" value="{{ mass }}"><br>
                           <input type="hidden" name="img_str" value="{{ img_str }}">  <!-- Carrying forward the image data -->
                           <input type="submit" value="Update">
                       </form>
                   </body>
               </html>
           ''', predicted_class_name=predicted_class_name, actual_calories=actual_calories, actual_kj=actual_kj,
                                      mass=mass, img_str=img_str)

    @app.route('/form', methods=['GET'])
    def display_form():
        # HTML form to submit user details
        return '''
            <form method="post" action="/analyze">
                Gender (M/F): <input type="text" name="gender"><br>
                Age: <input type="number" name="age"><br>
                Weight (kg): <input type="number" name="weight"><br>
                Height (cm): <input type="number" name="height"><br>
                <input type="submit" value="Submit">
            </form>
        '''

    @app.route('/analyze', methods=['POST'])
    def analyze():
        gender = request.form.get('gender', 'M').upper()
        age = float(request.form.get('age', 25))
        weight = float(request.form.get('weight', 70))
        height = float(request.form.get('height', 170))

        # Calculate Daily Calorie Needs
        if gender == "M":
            calorie_needs = 66.5 + (13.8 * weight) + (5 * height) - (6.8 * age)
        else:
            calorie_needs = 655.1 + (9.6 * weight) + (1.9 * height) - (4.7 * age)

        # Calculate BMI
        bmi = weight / ((height / 100) ** 2)

        # Connect to the SQLite database
        conn = sqlite3.connect('predictions.db')
        df = pd.read_sql_query("SELECT * FROM predictions", conn)
        conn.close()

        # Ensure there's data to analyze
        if df.empty:
            return "No prediction data available for analysis."

        # Perform analysis
        total_calories = df['calories'].sum()

        # Calculate Calorie Intake Difference
        calorie_intake_diff = total_calories - calorie_needs

        # Generate a pie chart for the food variety
        plt.figure(figsize=(10, 6))
        df['predicted_class'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Food Category Distribution")
        plt.ylabel('')
        plt.savefig('food_pie_chart.png')
        plt.close()

        # Encode the chart image for HTML rendering
        with open("food_pie_chart.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # Recommendations based on BMI and Calorie Intake Difference
        advice = ""
        if bmi < 18.5:
            if calorie_intake_diff >= 0:
                advice += "Vous êtes en sous-poids et vous consommez plus de calories que nécessaire. Nous encourageons votre comportement et vous recommandons de manger des aliments plus nutritifs !"
            else:
                advice+= "Vous êtes en sous-poids et consommez moins de calories que nécessaire. Envisagez d'augmenter l'apport calorique en consommant des aliments nutritifs."
        elif 18.5 <= bmi < 25:
            if calorie_intake_diff >= 0:
                advice += "Vous avez un poids normal, mais vous consommez plus de calories que nécessaire. Envisagez de maintenir ou de réduire légèrement votre apport calorique."
            else:
                advice += "Vous avez un poids normal et vous consommez moins de calories que nécessaire. Maintenez votre régime alimentaire équilibré actuel ou augmentez légèrement l'apport calorique si vous vous sentez en manque d'énergie."
        elif bmi >= 25:
            if calorie_intake_diff >= 0:
                advice += "Vous êtes en surpoids et consommez plus de calories que nécessaire. Envisagez de réduire l'apport calorique et de vous concentrer sur une alimentation équilibrée."
            else:
                advice += "Vous êtes en surpoids et vous consommez moins de calories que nécessaire. Continuez à faire du bon travail et concentrez-vous sur une alimentation saine et continue."
        # 各类食品建议摄入范围
        guidelines = {
            'Vegetable-Fruit': (450, 750),
            'Staples': (400, 600),  # Bread, Noodles-Pasta, and Rice
            'Others': (1000, 1200)  # Dairy product, Dessert, Egg, Fried food, Meat, Seafood, and Soup
        }
        # Reverse the labels for easier access
        reversed_labels = {v: k for k, v in labels.items()}
        # Calculate total mass and kj for each predicted class
        grouped = df.groupby('predicted_class').sum()

        # Create a dictionary to hold the advice
        advice_dict = {}

        # Using label names directly from your labels dictionary
        for food_category, (min_kj, max_kj) in guidelines.items():
            if food_category == 'Staples':
                categories = ['Bread', 'Noodles-Pasta', 'Rice']
            elif food_category == 'Others':
                categories = ['Dairy product', 'Dessert', 'Egg', 'Fried food', 'Meat', 'Seafood', 'Soup']
            else:
                categories = [food_category]  # For 'Vegetable-Fruit'

            # Calculate total kj for current category or categories
            total_kj = sum(grouped.loc[cat, 'kj'] for cat in categories if cat in grouped.index)

            # Determine advice based on total kj
            if total_kj < min_kj:
                advice_dict[food_category] = f"Consider increasing intake of {', '.join(categories)}."
            elif total_kj > max_kj:
                advice_dict[food_category] = f"Consider decreasing intake of {', '.join(categories)}."

        # Compile all advice into a string
        advice2 = " ".join(advice_dict.values())

        # Create an HTML response
        html = f"<html><body>"
        html += f"<h1>Nutritional Analysis</h1>"
        html += f"<h2>Your daily calorie needs: {calorie_needs:.2f} cal</h2>"
        html += f"<h2>Your BMI: {bmi:.2f}</h2>"
        html += f"<h2>Total Calories Intake: {total_calories} cal</h2>"
        html += f"<h2>Calorie Intake Difference: {calorie_intake_diff:.2f} cal</h2>"
        html += f"<p>{advice}</p>"
        # Add to the HTML response
        html += f"<p>{advice2}</p>"
        html += f"<img src='data:image/png;base64,{encoded_string}'/>"  # Display the pie chart
        html += f"<br><br><a href='/form'>Recalculate</a>"
        html += "</body></html>"

        return html

    logging.basicConfig(level=logging.INFO)
    scheduler = BackgroundScheduler()
    scheduler.start()
    # 初始化数据库
    def init_db_reminders():
        conn = sqlite3.connect('medicine_reminders.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reminders
                         (id INTEGER PRIMARY KEY, medicine TEXT, reminder_time DATETIME, dosage TEXT, message TEXT)''')  # 增加了剂量字段
        conn.commit()
        conn.close()

    init_db_reminders()

    def parse_medicine_frequency(text):
        # 示例的正则表达式
        frequency_pattern = r"(\d+/ [^\n]+)\n([^\n]+)"
        matches = re.findall(frequency_pattern, text)
        return [{"medicine": m[0], "dosage": m[1]} for m in matches]

    def add_reminder(medicine, frequency, dosage):
        # 根据频率计算 next_dose 时间
        next_dose = calculate_next_dose_time(frequency)  # 这是一个需要实现的新函数
        conn = sqlite3.connect('medicine_reminders.db')
        c = conn.cursor()
        c.execute("INSERT INTO reminders (medicine, reminder_time, dosage, message) VALUES (?, ?, ?, ?)",
                  (medicine, next_dose, dosage, "Il est temps de prendre vos médicaments！"))
        conn.commit()
        conn.close()

    def calculate_next_dose_time(frequency):
        # Return a time 24 hours from now
        return datetime.now() + timedelta(hours=24)

    def send_email(receiver, subject, body):
        try:
            sender = "jyiwen32@gmail.com"  # 使用你的发送者邮箱
            password = "snda afgv uwhz iglw"  # 使用你的密码

            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = receiver
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
            server.quit()
            logging.info(f"Email sent to {receiver} with subject: {subject}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def schedule_email_reminders():
        conn = sqlite3.connect('medicine_reminders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, medicine, reminder_time, dosage, message FROM reminders")

        for row in cursor.fetchall():
            id, medicine, reminder_time_str, dosage, message = row  # extract all row elements

            # Split the datetime string into the main part and the fractional seconds
            main_part, fractional_seconds = reminder_time_str.split('.')

            # Parse the main part of the datetime string
            reminder_time = datetime.strptime(main_part, '%Y-%m-%d %H:%M:%S')

            # Convert the fractional seconds to microseconds and add to reminder_time
            microseconds = int(fractional_seconds)
            reminder_time = reminder_time.replace(microsecond=microseconds)

            # Schedule the job
            scheduler.add_job(send_email, 'cron', day_of_week='mon-sun',
                              hour=reminder_time.hour, minute=reminder_time.minute,
                              args=['jyiwen32@gmail.com', 'Medicine Reminder',
                                    f"It's time to take your medicine: {medicine}, Dosage: {dosage}\n{message}"])
        conn.close()

    """
      # Run the function at the start to schedule all reminders
    def schedule_email_reminders():
        conn = sqlite3.connect('medicine_reminders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, medicine, reminder_time, dosage, message FROM reminders")

        for row in cursor.fetchall():
            id, medicine, reminder_time_str, dosage, message = row

            reminder_time = calculate_next_dose_time(None)  # 测试用：计算1分钟后的时间

            scheduler.add_job(send_email, 'date', run_date=reminder_time,
                              args=['jyiwen32@gmail.com', 'Medicine Reminder',
                                    f"It's time to take your medicine: {medicine}, Dosage: {dosage}\n{message}"])
            logging.info(f"Scheduled email to be sent at {reminder_time}")
        conn.close()
    """
    schedule_email_reminders()

    @app.route('/predict_img_api', methods=['POST'])
    def predict_img_api():
        print("Predict Image function callled through API")  # Debugging line


        file = request.files['image']
        img = Image.open(file.stream)

        img = img.resize((256, 256))  # Resize to the size your model expects
        img = np.array(img)  # Convert to numpy array
        img = img / 255.0  # Normalize the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        # Make prediction
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_class_name = labels[predicted_class[0]]

        print(predicted_class_name)


        return jsonify({"class": predicted_class_name})
    @app.route('/detect-text', methods=['POST'])
    def detect_text():
        # 设置图片路径
        file_path = "data/Ordonnance.jpg"

        # 读取图片文件
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        # 使用Vision API
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            full_text = texts[0].description
            medicine_details = parse_medicine_frequency(full_text)

            for detail in medicine_details:
                medicine = detail["medicine"]
                dosage = detail["dosage"]
                frequency = "Some default value or parsed value"  # You need to define how to get this
                next_dose = calculate_next_dose_time(frequency)
                add_reminder(medicine, frequency, dosage)
            # 在这里使用 APScheduler 安排提醒
            #scheduler.add_job(reminder_function, trigger='date', run_date=next_dose, args=[user_details])

            return jsonify({"texts": full_text, "frequencies": frequency})
        else:
            return "No text found", 404

    @app.route('/detect_text_api', methods=['POST'])
    def detect_text_api():
        # 设置图片路径

        '''
        # 读取图片文件
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
        '''

        file = request.files['image']
        img = Image.open(file.stream)

        # 使用Vision API
        image = vision.Image(content=img)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # 返回识别结果
        if texts:
            return jsonify({"texts": texts[0].description})
        else:
            return "No text found", 404



    @app.route('/delete-all-reminders', methods=['GET'])
    def delete_all_reminders():
        try:
            conn = sqlite3.connect('medicine_reminders.db')
            c = conn.cursor()

            # 删除所有记录
            c.execute("DELETE FROM reminders")

            conn.commit()
            conn.close()

            return jsonify({'status': 'success', 'message': 'All reminders deleted.'}), 200

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


    @app.route('/clear_predictions', methods=['POST'])
    def clear_data():
        clear_predictions()  # Call the function to clear data
        return "Predictions data cleared successfully!"

    @app.route('/search', methods=['GET'])
    def search():
        # 获取查询参数
        location = request.args.get('location', 'paris')  # 默认值为'paris'
        medecin_type = request.args.get('medecin_type', 'medecin-generaliste')  # 默认值为'medecin-generaliste'

        # 配置Selenium
        options = Options()
        options.headless = True  # 无头模式
        browser = webdriver.Firefox(options=options)

        try:
            # 构造目标网址
            url = f"https://www.doctolib.fr/{medecin_type}/{location}?availabilities=3"

            # 打开网页
            browser.get(url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dl-search-result-presentation"))
            )

            # 解析网页
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            # 提取医生的名字和可用时间段
            doctors_info = []

            # 找到外层的 'col-8 col-padding search-results-col-list' 容器
            search_results_list = soup.find_all("div", class_="col-8 col-padding search-results-col-list")

            for results_list in search_results_list:
                # 在每个外层容器中寻找 'dl-layout-container'
                layout_containers = results_list.find_all("div", class_="dl-layout-container")
                for layout_container in layout_containers:
                    # 对每个医生信息块进行遍历
                    doc_blocks = layout_container.find_all("div", class_="dl-layout-item dl-layout-size-xs-12")
                    for doc_block in doc_blocks:
                        presentation_container = doc_block.find("div", class_="dl-search-result-presentation")
                        if presentation_container:
                            name_section = presentation_container.find("h3",
                                                                       class_="dl-text dl-text-body dl-text-regular dl-text-s dl-text-primary-110")
                            name = name_section.text.strip() if name_section else "Name not found"
                        else:
                            continue  # 如果没有找到名称容器则跳过

                        # 查找该医生对应的可用时间段
                        calendar_container = doc_block.find("div", class_="dl-search-result-calendar")
                        time_slots = []
                        if calendar_container:
                            # 遍历每个'日'的容器
                            days_containers = calendar_container.find_all("div", class_="availabilities-day")
                            for day_container in days_containers:
                                # 在每个'日'的容器中遍历可用时间段
                                slots = day_container.find_all("div", class_="availabilities-slot")
                                for slot in slots:
                                    time = slot.get("aria-label", "No time found").strip()
                                    time_slots.append(time)

                        if name != "Name not found" and time_slots:
                            doctors_info.append({"name": name, "availability": time_slots, "url": url})

            return jsonify(doctors_info)

        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            browser.quit()


    return app




class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    video_class = db.Column(db.String(120), nullable=False)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)


