from flask import Flask, request
from indexing import search, get_keywords, comments 
from flask import jsonify
import json 

app = Flask(__name__)

@app.route("/home", methods = ['POST'])
def hello():

    body = request.json
    search_input = body['search']

    search_terms = search_input.split()
    search_string = '+'.join(search_terms)

    output = search(search_string)
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port = 5001)