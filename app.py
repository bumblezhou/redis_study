import json
import os
import uuid
import sys
import os
from io import BytesIO
from os import path
from elasticsearch import Elasticsearch

from flask import Flask, jsonify, render_template, request, send_file

template_folder = os.path.join("./", 'templates')
static_folder = os.path.join("./", 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Replace these with your actual username and password
username = 'elastic'
password = 'usKuJ3daCL4vf98kQ0Dk'

# Create the connection instance
es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=(username, password)
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    search_key_words = request.args.get('query', '')
    res = es.search(index="documents", query={"bool": {"should": [{"match": {"ContractContent": search_key_words}}]}})
    # print("Got %d Hits:" % res['hits']['total']['value'])
    items = []
    for hit in res['hits']['hits']:
        print("%(ProjectName)s: %(ContractName)s %(PublishDate)s" % hit["_source"])
        items.append(hit["_source"])
    return jsonify([dict(item) for item in items])

# run the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
    # app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)