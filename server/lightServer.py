#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

class Update(Resource):
    def post(self):
        json_data = request.get_json()
        return jsonify(json_data)

api.add_resource(Update, '/update') # Route_1

if __name__ == '__main__':
     app.run(port='5000')