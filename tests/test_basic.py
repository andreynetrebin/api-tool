import unittest
from unittest.mock import patch
from api_tool import RestApiTool, ApiError


class TestRestApiTool(unittest.TestCase):
    @patch('requests.Session')
    def test_get_request(self, mock_session):
        mock_response = mock_session.return_value
        mock_response.request.return_value.status_code = 200
        mock_response.request.return_value.json.return_value = {'key': 'value'}

        api = RestApiTool("http://test.com")
        response = api.get("/test")

        self.assertEqual(response, {'key': 'value'})
