import os
import time
import yaml

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

class BerryNetProvider():
    """Berry Net Provider"""

    def __init__(self, server='localhost', port=1883, path='/home/pi/repos/BerryNet'):
        """Create a berry net provider instance"""

        self._server = server
        self._port = port
        self._path = path
        self._sources = set(['boardcam', 'ipcamera', 'local'])
        self._topics = {
            'boardcam': ('berrynet/event/camera', 'snapshot_boardcam'),
            'ipcamera': ('berrynet/event/camera', 'snapshot_ipcam'),
            'local':    ('berrynet/event/localImage', None)
        }

    def analyze(self, img_source=None, path=None, client_id="", save_img=False, save_path=None, draw_bound=False, **kwargs):
        """Analyze a new image from the source"""

        img_source = img_source.lower()
        if img_source not in self._sources:
            assert "The img_source provided is invalid."

        # Get the topic and message for the image source
        topic, message = self._topics[img_source]

        # If local selected the message is the path of the image
        if not message:
            if path:
                message = path
            else:
                assert "The path is required for img_source: local."

        try:
            publish.single(topic, payload=message, hostname=self._server, port=self._port, client_id=client_id, **kwargs)
            
            print('Waiting for results...')
            results = self._receive_result()
            print('Done.')

            # TODO: also return image location / possibly read file in
            # TODO: handle deletion of old images

            return results

        except Exception:
            # Failed to capture and/or analyze return no results
            return None

    def _receive_result(self, topic='berrynet/dashboard/inferenceResult', **kwargs):
        """Subscribe the broker and receive the results"""

        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()
        results = yaml.load(message)

        return results

    def _receive_img(self, topic='berrynet/dashboard/inference', **kwargs):
        """Subscribe the inference topic to receive the image"""
        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()

        return message

    def open(self):
        # Start the static berry net service if required and warm up
        os.system('berrynet-manager start')
        print('Warming up...')
        time.sleep(10)
        print('Done.')

    def close(self):
        # Stop the static berry net service
        os.system('berrynet-manager stop')