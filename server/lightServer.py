#!/usr/bin/env python3

import sys
import serial
import signal
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)
# serial_bus = serial.Serial('/dev/ttyUSB0', 19200)

class Update(Resource):
    def post(self):
        json_data = request.get_json()
        status = json_data['status']
        countdown = json_data['countdown']
        
        print(status)
        print(countdown)
        
        # serial_bus.write(0) # write bytes

        return

api.add_resource(Update, '/update') # Route_1

def handler(signal, frame):
    # serial_bus.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


if __name__ == '__main__':
     app.run(port='5000')