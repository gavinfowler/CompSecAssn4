from flask import Flask,request,send_from_directory
import itertools
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def home():
    return send_from_directory('.', 'client/index.html')

if __name__ == "__main__":
    app.run(debug=True)