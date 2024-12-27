import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
import numpy as np

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 路由：主页
@app.route('/')
def index():
    return render_template('index.html')

# 路由：处理图片
@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "未选择文件"

    file = request.files['file']
    if file.filename == '':
        return "文件名为空"

    # 保存上传的图片
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # 获取美颜参数
    brightness = int(request.form.get('brightness', 50)) - 50
    contrast = float(request.form.get('contrast', 50)) / 50.0
    blur = int(request.form.get('blur', 0))

    # 使用 OpenCV 处理图片
    img = cv2.imread(file_path)
    img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    if blur > 0:
        img = cv2.GaussianBlur(img, (blur * 2 + 1, blur * 2 + 1), 0)

    # 保存处理后的图片
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"processed_{file.filename}")
    cv2.imwrite(output_path, img)

    return render_template('index.html', original=file.filename, processed=f"processed_{file.filename}")

# 路由：下载图片
@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
