from flask import Flask, request
from indexing import search, get_keywords, comments 
from flask import jsonify
from flask_cors import CORS
import json 

app = Flask(__name__)
CORS(app)

cache = {}

@app.route("/")
def index():
    return jsonify({ "hi": True })

@app.route("/home", methods = ['POST'])
def hello():

    body = request.json
    search_input = body['search']

    if search_input in cache:
        output = cache[search_input]
    else:
        search_terms = search_input.split()
        search_string = '+'.join(search_terms)

        output = search(search_string)
        
        symp_file = open("sympgraph_dict.json", "r")
        sympgraph_dict = eval(symp_file.read())

        id_file = open("keyword_id.json", "r")
        d1_id = eval(id_file.read())
        name_file = open("keyword_name.json", "r")
        d1_name = eval(name_file.read())

        top_keywords = []

        
        if search_input in d1_name:
            search_val = d1_name[search_input]
            if search_val in sympgraph_dict:
                l1 = sorted(sympgraph_dict[search_val], key = lambda x: x[1], reverse = True)
                if len(l1) > 7:
                    l2 = l1[:7]
                else:
                    l2 = l1
                for j in l2:
                    top_keywords.append(d1_id[j[0]])

        output['top_keyword'] = top_keywords
        cache[search_input] = output

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5001)