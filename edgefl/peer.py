import requests
import json
import os
import threading
import os
import shutil
import torch
import time
from flask import Flask, send_file

app = Flask(__name__)

# Serve the requested file using Flask
@app.route('/latest_model', methods=['GET'])
def serve_file():
    try:
        return send_file("model-latest.pth")
    except FileNotFoundError:
        return 'File not found', 404


class Peer:
    def __init__(self, REGISTRATION_ADDRESS, LOCAL_PORT, FUNC_CONFIG):
        self.peers = []
        self.LOCAL_PORT = LOCAL_PORT
        self.REGISTRATION_ADDRESS = "http://" + REGISTRATION_ADDRESS
        self.FUNC_CONFIG = FUNC_CONFIG

        with open(self.FUNC_CONFIG, "r") as f:
            func_conf = f.read()

        func_namespace = {}
        exec(func_conf, func_namespace)
        self.FedSync = func_namespace["FedAvg"]


    def start(self):

        # Register with the registration node
        self.register_with_registration()
        print("get registration")
        # Start the Flask app to serve file requests
        threading.Thread(target=self.start_flask_app).start()

    def register_with_registration(self):
        # Send a registration request to the registration node
        hostname = os.environ['HOSTNAME']
        response = requests.post(self.REGISTRATION_ADDRESS + '/register', json={'hostname': hostname})
        self.peers = response.json()['peers']
        print('Registered with registration node. Active peers:', self.peers)


    def start_flask_app(self):
        app.run(host="0.0.0.0", port=self.LOCAL_PORT)

    def aggregation_func(self):
        response = requests.get(self.REGISTRATION_ADDRESS + '/peers')
        self.peers = response.json()['peers']
        W_LOCALS = []
        for peer in self.peers:
            print('Fetch model from', peer["hostname"])
            url = 'http://' + peer["hostname"] + '/latest_model'
            start_time = time.time()
            self.fetch(url)
            cost_time = time.time() - start_time
            print('Get model from', peer["hostname"], "cost_time: ", cost_time)
            W_LOCALS.append(torch.load("model.pth"))

        W_latest = self.FedSync(W_LOCALS)
        return W_latest

    def fetch(self, url):
        with requests.get(url, stream=True) as r:
            with open("model.pth", 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def unregister_peer(self):
        hostname = os.environ['HOSTNAME']
        response = requests.post(self.REGISTRATION_ADDRESS + '/unregister', json={'hostname': hostname})
        self.peers = response.json()['peers']
        print('Unregistered with registration node. Active peers:', self.peers)
