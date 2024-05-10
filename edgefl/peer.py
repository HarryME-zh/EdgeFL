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

# Define a Flask route to serve the latest model file
@app.route('/latest_model', methods=['GET'])
def serve_file():
    try:
        return send_file("model-latest.pth")  # Serve the latest model file if found
    except FileNotFoundError:
        return 'File not found', 404  # Return a 404 error if the file is not found

class Peer:
    def __init__(self, REGISTRATION_ADDRESS, LOCAL_PORT, FUNC_CONFIG):
        """
        Initialize Peer class with registration address, 
        local port, and function configuration file.
        """
        self.peers = []
        self.LOCAL_PORT = LOCAL_PORT
        self.REGISTRATION_ADDRESS = "http://" + REGISTRATION_ADDRESS
        self.FUNC_CONFIG = FUNC_CONFIG

        # Read function configuration from file and load it dynamically
        with open(self.FUNC_CONFIG, "r") as f:
            func_conf = f.read()

        func_namespace = {}
        exec(func_conf, func_namespace)
        self.FedSync = func_namespace["FedAvg"]  # Assign FedAvg function from the configuration

    def start(self):
        """
        Start the Peer instance by registering with 
        the registration node and starting Flask app.
        """
        # Register with the registration node
        self.register_with_registration()
        print("Registered with registration node. Active peers:", self.peers)
        
        # Start the Flask app to serve model file requests
        threading.Thread(target=self.start_flask_app).start()

    def register_with_registration(self):
        """
        Send a registration request to the registration
        node and update the list of active peers.
        """
        hostname = os.environ['HOSTNAME']
        response = requests.post(self.REGISTRATION_ADDRESS + '/register', json={'hostname': hostname})
        self.peers = response.json()['peers']

    def start_flask_app(self):
        """
        Start the Flask app to serve model file requests.
        """
        app.run(host="0.0.0.0", port=self.LOCAL_PORT)

    def aggregation_func(self):
        """
        Perform model aggregation by fetching models
        from peers and applying FedAvg.
        """
        response = requests.get(self.REGISTRATION_ADDRESS + '/peers')
        self.peers = response.json()['peers']
        W_LOCALS = []

        # Fetch models from peers
        for peer in self.peers:
            url = 'http://' + peer["hostname"] + '/latest_model'
            start_time = time.time()
            self.fetch(url)  # Fetch model from peer
            cost_time = time.time() - start_time
            print('Get model from', peer["hostname"], "cost_time:", cost_time)
            W_LOCALS.append(torch.load("model.pth"))  # Load fetched model

        # Aggregate models using FedAvg
        W_latest = self.FedSync(W_LOCALS)
        return W_latest

    def fetch(self, url):
        """
        Fetch model file from the given URL.
        """
        with requests.get(url, stream=True) as r:
            with open("model.pth", 'wb') as f:
                shutil.copyfileobj(r.raw, f)  # Save fetched model to file

    def unregister_peer(self):
        """
        Unregister the peer with the registration node.
        """
        hostname = os.environ['HOSTNAME']
        response = requests.post(self.REGISTRATION_ADDRESS + '/unregister', json={'hostname': hostname})
        self.peers = response.json()['peers']
        print('Unregistered with registration node. Active peers:', self.peers)
