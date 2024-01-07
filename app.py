import requests
from flask import *
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
# Other necessary imports and model definition code goes here
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

    model = load_model("./model-re-image.h5")
    model_sport = load_model("./sport_model.h5")
    classes_sport = sorted(os.listdir("./data/sport"))
    model = load_model("./model-re-image.h5")

    model_sport = load_model("./sport_model.h5")

    classes_sport = sorted(os.listdir("./data/sport/"))


    credentials = service_account.Credentials.from_service_account_file("data/recotexte-409521-6e14f0a168bc.json")
    client = vision.ImageAnnotatorClient(credentials=credentials)

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
            # video_path = os.path.join(r"C:\Users\Jiang\flask-vue-crud\data\sport", video_class)
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
        #video_path = os.path.join(r"C:\Users\Jiang\flask-vue-crud\data\sport", video_class, video_filename)
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

        # 获取最近一次观看的视频类别
        last_watched_record = user_watches[-1]  # 假设最后一条记录是最近的一次观看
        last_watched_class = last_watched_record.video_class

        # 获取该类别下所有视频
        #video_path = os.path.join(r"C:\Users\Jiang\flask-vue-crud\data\sport", last_watched_class)
        video_path = os.path.join("data/sport", last_watched_class)
        try:
            all_videos = os.listdir(video_path)
        except FileNotFoundError:
            return jsonify({"error": "Video class directory not found"}), 404

        # 如果视频类别下没有视频
        if not all_videos:
            return jsonify({"error": "No videos found for the class"}), 404

        # 从该类别中选择几个随机视频推荐给用户
        num_recommendations = min(5, len(all_videos))  # 推荐数量，不超过该类别视频数量
        recommendations = random.sample(all_videos, num_recommendations)

        # 构建推荐视频的信息列表
        recommendations_info = [{"class": last_watched_class, "filename": video} for video in recommendations]

        # 构建推荐视频的信息列表，并为每个视频添加URL
        recommendations_info = []
        for video in recommendations:
            video_url = f"/video/{last_watched_class}/{video}"  # 构造视频的URL路径
            recommendations_info.append({
                "class": last_watched_class,
                "filename": video,
                "url": video_url  # 添加URL到信息中
            })

        return jsonify(recommendations_info)

    # todo: adapt this so that a picture is sent instead
    @app.route('/predict_img', methods=['GET'])
    def predict_img():
        print("Predict Image function called")  # Debugging line
        image_path = 'data/b.jpeg'  # Change to your image file name

        if not os.path.isfile(image_path):
            return "Image does not exist."
        print(os.path.abspath(image_path))  # Add this for debugging

        # Open the image file
        img = Image.open(image_path)
        display_img = img.copy()  # Make a copy for displaying
        img = img.resize((256, 256))  # Resize to the size your model expects
        img = np.array(img)  # Convert to numpy array
        img = img / 255.0  # Normalize the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        # Make prediction
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_class_name = labels[predicted_class[0]]

        # Convert the image to a format that can be displayed in HTML
        buffered = io.BytesIO()
        display_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Create an HTML response
        html = f"<html><body>"
        html += f"<h2>Predicted Class: {predicted_class_name}</h2>"
        html += f"<img src='data:image/jpeg;base64,{img_str}'/>"
        html += "</body></html>"

        return html

    # todo: adapt this so a picture is sent instead
    @app.route('/detect-text', methods=['GET'])
    def detect_text():
        # 设置图片路径
        # file_path = "C:/Users/Jiang/flask-vue-crud/data/Ordonnance.jpg"
        file_path = "data/Ordonnance.jpg"

        # 读取图片文件
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        # 使用Vision API
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # 返回识别结果
        if texts:
            return jsonify({"texts": texts[0].description})
        else:
            return "No text found", 404

    return app
class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    video_class = db.Column(db.String(120), nullable=False)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)


