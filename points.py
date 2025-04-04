import geojson
import pprint as pp
import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS


validation_points = []
tile_ids = ['23608577','23608578','23608580','23608592','23612004','23612006','23612035']

for id in tile_ids:
    with open(f'data_set/{id}/{id}_validations.geojson', 'r') as file:
        geojson_data = geojson.load(file)

    for part in geojson_data['features']:
        coord = part["geometry"]["coordinates"]
        validation_points.append({"longitude":coord[0],"latitude":coord[1]})

app = Flask(__name__)
CORS(app)

@app.route('/api/array')
def get_array():
    global validation_points
    return jsonify(validation_points)

if __name__ == '__main__':
    app.run(debug=True)
