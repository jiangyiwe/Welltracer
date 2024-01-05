import io
import os
from google.cloud import vision
#%%
# 设置你的API密钥路径
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Jiang\flask-vue-crud\data\recotexte-409521-6e14f0a168bc.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data/recotexte-409521-6e14f0a168bc.json"
#%%
# 实例化Vision Client
client = vision.ImageAnnotatorClient()

#%%
# 图片所在的路径
# file_path = r'C:\Users\Jiang\flask-vue-crud\data\Ordonnance.jpg'
file_path = 'data/Ordonnance.jpg'
#%%

# 读取图片
with io.open(file_path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# 发起请求进行文本识别
response = client.text_detection(image=image, image_context={"language_hints": ["fr"]})

texts = response.text_annotations

# 输出识别到的文本
for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                 for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(response.error.message))