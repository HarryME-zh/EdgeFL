import unittest
import json
from flask import Flask
from edgefl.registation import registration, register, unregister, get_peers

class TestRegistration(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    # Test case for the /register route
    def test_register(self):
        with self.app.test_request_context('/register', method='POST', data=json.dumps({'hostname': 'test_peer'}), content_type='application/json'):
            response = register()
            data = json.loads(response.get_data(as_text=True))

            # Check if the peer was registered and returned in the response
            self.assertEqual(response.status_code, 200)
            self.assertIn('peers', data)
            self.assertEqual(len(data['peers']), 1)
            self.assertEqual(data['peers'][0]['hostname'], 'test_peer')

    # Test case for the /unregister route
    def test_unregister(self):
        # Register a test peer first
        with self.app.test_request_context('/register', method='POST', data=json.dumps({'hostname': 'test_peer'}), content_type='application/json'):
            register()

        # Then, unregister the test peer
        with self.app.test_request_context('/unregister', method='POST', data=json.dumps({'hostname': 'test_peer'}), content_type='application/json'):
            response = unregister()
            data = json.loads(response.get_data(as_text=True))

            # Check if the peer was unregistered and not returned in the response
            self.assertEqual(response.status_code, 200)
            self.assertIn('peers', data)
            self.assertEqual(len(data['peers']), 0)

    # Test case for the /peers route
    def test_get_peers(self):
        # Register some test peers
        with self.app.test_request_context('/register', method='POST', data=json.dumps({'hostname': 'test_peer1'}), content_type='application/json'):
            register()

        with self.app.test_request_context('/register', method='POST', data=json.dumps({'hostname': 'test_peer2'}), content_type='application/json'):
            register()

        # Get the list of active peers
        with self.app.test_request_context('/peers', method='GET'):
            response = get_peers()
            data = json.loads(response.get_data(as_text=True))

            # Check if the response contains the registered peers
            self.assertEqual(response.status_code, 200)
            self.assertIn('peers', data)
            self.assertEqual(len(data['peers']), 2)
            self.assertIn({'hostname': 'test_peer1'}, data['peers'])
            self.assertIn({'hostname': 'test_peer2'}, data['peers'])

if __name__ == '__main__':
    unittest.main()
