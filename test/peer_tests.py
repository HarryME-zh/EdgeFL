import unittest
from unittest.mock import patch
from edgefl import Peer

class TestPeer(unittest.TestCase):

    def setUp(self):
        # Set up any test data or configurations here
        self.REGISTRATION_ADDRESS = "http://registration.address"
        self.LOCAL_PORT = 5000
        self.peer = Peer(self.REGISTRATION_ADDRESS, self.LOCAL_PORT)

    def tearDown(self):
        # Clean up after each test (if needed)
        pass

    # Test case for register_with_registration method
    def test_register_with_registration(self):
        # Create a mock response for the requests.post
        with patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'peers': ['peer1', 'peer2']}
            self.peer.register_with_registration()

            # Assert that the peer's peers attribute is updated correctly
            self.assertEqual(self.peer.peers, ['peer1', 'peer2'])

    # Test case for aggregation_func method
    def test_aggregation_func(self):
        # Create a mock response for the requests.get
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {'peers': [{'hostname': 'peer1'}, {'hostname': 'peer2'}]}

            # Mock the fetch method
            with patch.object(self.peer, 'fetch') as mock_fetch:
                # Mock the Torch model loading
                with patch('torch.load') as mock_load:
                    # Set up the return value for the mock model loading
                    mock_load.return_value = your_mocked_torch_model
                    self.peer.aggregation_func()

                    # Assert that fetch was called twice with the correct URLs
                    mock_fetch.assert_any_call('http://peer1/latest_model')
                    mock_fetch.assert_any_call('http://peer2/latest_model')

if __name__ == '__main__':
    unittest.main()
