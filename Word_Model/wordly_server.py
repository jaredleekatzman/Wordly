#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import sys
sys.path.append('./Model/')
from wordly import Wordly

app = Flask(__name__, static_url_path = "")
model = Wordly()

@app.errorhandler(400)
def not_found(error):
    return jsonify( { 'error': 'Bad request' } ), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify( { 'error': 'Not found' } ), 404

@app.route('/wordly/look_up', methods = ['POST'])
def look_up():
    if not request.json or not 'query' in request.json:
        print request.json
        abort(400)
    
    k = request.json.get('k', 5)
    results = model.look_up(request.json['query'],int(k))
    json = {word : dist for (word, dist) in results}

    return jsonify(json), 201
    
if __name__ == '__main__':
    print 'Initializing Wordly model...'
    model.initialize_model(json = 'Model/model.json',
        weights = 'Model/weights.hdf5',
        embed_path = 'Model/embeddings.hdf5', verbose = True)

    print 'Running Server...'
    app.run(debug = True)