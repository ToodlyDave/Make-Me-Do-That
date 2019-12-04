from flask import Flask
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

@app.route('/', methods = ["GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def connection():
    return json.dumps({"payload":"Hi there", "type":"SUCCESS"})

if __name__=="__main__":
    app.run()