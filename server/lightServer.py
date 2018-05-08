#!/usr/bin/env python3

import sys
import serial
import signal
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)
serial_bus = serial.Serial('/dev/cu.SLAB_USBtoUART', 19200)

class Update(Resource):
    def post(self):
        json_data = request.get_json()
        status = json_data['status']
        print(status)

        if (status == 'ESTIMATE'):
            countdown = chr(int(json_data['countdown']) // 60)
            print(ord(countdown))

            serial_bus.write(countdown.encode()) # write byte

        elif (status == 'DOCKED'):
            serial_bus.write(chr(0).encode()) # write byte

        else:
            serial_bus.write(chr(255).encode()) # write byte

        return

api.add_resource(Update, '/update') # Route_1

def handler(signal, frame):
    serial_bus.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


if __name__ == '__main__':
     app.run(port='5000')
