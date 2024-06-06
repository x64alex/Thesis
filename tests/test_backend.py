import unittest
from unittest.mock import patch
from your_flask_app import app

class BackendTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_response(self):
        data = {'user_input': 'test input'}
        response = self.app.post('/get_response', json=data)
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertIn('response', json_response)
        self.assertIsInstance(json_response['response'], str)

    @patch('your_flask_app.jcml.update_configuration')
    def test_update_json(self, mock_update_configuration):
        data = {'key': 'value'} 
        response = self.app.post('/update_json', json=data)
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response['message'], 'JSON file updated successfully')
        mock_update_configuration.assert_called_once_with(data)

if __name__ == '__main__':
    unittest.main()
