# Test file for FreedomPay Integration

import unittest
from unittest.mock import patch, MagicMock

import frappe

from .freedompay_api import FreedomPayAPI
from .connection import FreedomPayConnection


class TestFreedomPayConnection(unittest.TestCase):
    def setUp(self):
        # Create mock settings
        self.mock_settings = MagicMock()
        self.mock_settings.get_password.return_value = "test_secret_key"
        self.mock_settings.base_url = "https://api.freedompay.uz"

    @patch('frappe.get_doc')
    def test_generate_signature(self, mock_get_doc):
        mock_get_doc.return_value = self.mock_settings

        conn = FreedomPayConnection()
        data = {
            'pg_merchant_id': '123',
            'pg_amount': '100.00'
        }

        signature = conn.generate_signature("https://api.freedompay.uz/init_payment.php", data)

        # Check that signature is generated (MD5 hash is 32 characters)
        self.assertEqual(len(signature), 32)
        self.assertTrue(signature.isalnum())


class TestFreedomPayAPI(unittest.TestCase):
    def setUp(self):
        self.mock_settings = MagicMock()
        self.mock_settings.merchant_id = "12345"
        self.mock_settings.get_password.return_value = "test_secret_key"
        self.mock_settings.base_url = "https://api.freedompay.uz"

    @patch('frappe.get_doc')
    @patch('freedompay_integration.connection.FreedomPayConnection.post')
    def test_create_payment(self, mock_post, mock_get_doc):
        mock_get_doc.return_value = self.mock_settings

        # Mock successful response
        mock_post.return_value = ("SUCCESS", MagicMock(data={'pg_payment_id': 'test_123'}))

        api = FreedomPayAPI()
        code, payment, feedback = api.create_payment({
            'amount': '100.00',
            'currency': 'UZS',
            'description': 'Test payment'
        })

        self.assertEqual(code, "SUCCESS")
        self.assertEqual(payment['pg_payment_id'], 'test_123')
        self.assertEqual(feedback.message, "Payment Created Successfully")


if __name__ == '__main__':
    unittest.main()
