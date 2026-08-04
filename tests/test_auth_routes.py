import unittest

from routers.auth import extract_token_from_request


class DummyHeaders(dict):
    def get(self, key, default=None):
        return super().get(key.lower(), default)


class DummyRequest:
    def __init__(self, headers=None, query_params=None):
        self.headers = DummyHeaders(headers or {})
        self.query_params = DummyHeaders(query_params or {})


class AuthRouteTokenTests(unittest.TestCase):
    def test_extract_token_from_authorization_header(self):
        request = DummyRequest(headers={"authorization": "Bearer abc123"})
        self.assertEqual(extract_token_from_request(request), "abc123")

    def test_extract_token_from_query_param(self):
        request = DummyRequest(query_params={"token": "xyz789"})
        self.assertEqual(extract_token_from_request(request), "xyz789")

    def test_extract_token_returns_none_when_missing(self):
        request = DummyRequest()
        self.assertIsNone(extract_token_from_request(request))


if __name__ == "__main__":
    unittest.main()
