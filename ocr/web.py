from flask import Flask, request
from PIL import Image
from auth import *

app = Flask(__name__)


@app.route("/imgcode", methods=['POST'])
def upload_img():
    try:
        return get_text(request.files['img'].read())
    except Exception:
        print("验证码解析异常...")
        return "0"


@app.route("/help")
def help():
    return """
    <h1> 帮助文档 </h1>
    <ul>
        <li>识别地址: /imgcode, 需要POST form表单提交，图片name为img</li>
        <li>若返回为0，则是识别失败，请重新提交新的验证码</li>
    </ul>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0")
