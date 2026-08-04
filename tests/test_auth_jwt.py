import unittest
from datetime import timedelta

from core.security import (
    create_access_token,
    hash_password,
    verify_password,
    verify_token,
)


class JwtTokenTests(unittest.TestCase):
    def test_create_and_verify_access_token(self):
        payload = {"sub": "42", "role": "user"}
        token = create_access_token(payload, expires_delta=timedelta(minutes=5))
        decoded = verify_token(token)

        self.assertEqual(decoded["sub"], "42")
        self.assertEqual(decoded["role"], "user")

    def test_password_hashing_and_verification(self):
        password = "super-secret"
        hashed_password = hash_password(password)

        self.assertTrue(verify_password(password, hashed_password))
        self.assertFalse(verify_password("wrong-password", hashed_password))


if __name__ == "__main__":
    unittest.main()
