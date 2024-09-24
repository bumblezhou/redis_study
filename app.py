import json
import os
import uuid
import sys
import os
from io import BytesIO
from os import path
import redis

from flask import Flask, jsonify, render_template, request, send_file

template_folder = os.path.join("./", 'templates')
static_folder = os.path.join("./", 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

client = redis.Redis(host='localhost', port=6379)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    search_key_words = request.args.get('query', '')
    res = client.ft().search(search_key_words)
    items = res.docs
    # print(items)
    return jsonify([json.loads(item.json) for item in items])

# run the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
    # app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)