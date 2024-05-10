from flask import Flask, jsonify, request
import json

app = Flask(__name__)

class Registration:
    def __init__(self):
        """
        Initialize Registration class with an empty list of peers.
        """
        self.peers = []

    def register_peer(self, peer_info):
        """
        Register a peer with the registration server.
        """
        self.peers.append(peer_info)
        print('Registered peer:', peer_info)

    def unregister_peer(self, peer_info):
        """
        Unregister a peer from the registration server.
        """
        if peer_info in self.peers:
            self.peers.remove(peer_info)
            print('Unregistered peer:', peer_info)

    def get_active_peers(self):
        """
        Get the list of active peers registered with the server.
        """
        return self.peers

# Create a Registration instance
registration = Registration()

@app.route('/register', methods=['POST'])
def register():
    """
    Endpoint to handle peer registration requests.
    """
    data = json.loads(request.data)
    ip_address = request.remote_addr
    port = str(request.environ.get('REMOTE_PORT'))
    peer_info = {
        'address': ip_address,
        'port': port,
        'hostname': data['hostname']
    }
    registration.register_peer(peer_info)
    return jsonify({'peers': registration.get_active_peers()})

@app.route('/unregister', methods=['POST'])
def unregister():
    """
    Endpoint to handle peer unregistration requests.
    """
    data = json.loads(request.data)
    ip_address = request.remote_addr
    port = str(request.environ.get('REMOTE_PORT'))
    peer_info = {
        'address': ip_address,
        'port': port,
        'hostname': data['hostname']
    }
    registration.unregister_peer(peer_info)
    return jsonify({'peers': registration.get_active_peers()})

@app.route('/peers', methods=['GET'])
def get_peers():
    """
    Endpoint to retrieve the list of active peers.
    """
    return jsonify({'peers': registration.get_active_peers()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
