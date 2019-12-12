from flask import Flask, request
from flask_cors import CORS, cross_origin
from io import BytesIO
from PIL import Image
import json
import base64
import PIL

app = Flask(__name__)

@app.route('/', methods = ["POST"])

def connection():
    if request.method == "POST":
        data = request.get_json(force=True)
        print("\n\n\n\n   The message: ", data["status"])

        image = Image.open(BytesIO(base64.b64decode(data["payload"])))
        image.save("the test.jpg")

        return json.dumps({"payload":"We hear you bruh", "type":"SUCCESS"})
    else:
        print("\n\nNot post")
    
    return json.dumps({"payload":"We don't hear you", "type":"Error!!!"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000")