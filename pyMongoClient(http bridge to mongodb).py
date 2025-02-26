from flask import Flask, jsonify
from flask import request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://Entropy:<NatanforEveryone107>@entropy-hsc034.ib3jo.mongodb.net/?appName=Entropy-HSC034"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["esp32"]
collection = db["sensor"]

@app.route('/')
def check() :
    return "bisa cuy!!!!"

@app.route('/data', methods=['post'])
def collect_data() :
    data = request.json
    #send to Mongodb

    collection.insert_one(data)
    return jsonify({"status": "succes", "message": "data saved"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6000)  