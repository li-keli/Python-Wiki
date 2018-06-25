from flask import Flask, request
from PIL import Image
from auth import *

app = Flask(__name__)


@app.route("/imgcode", methods=['POST'])
def upload_img():
    f = request.files['file'].read()
    im = Image.open(BytesIO(f))
    return get_text(f)

if __name__ == "__main__":
    app.run()