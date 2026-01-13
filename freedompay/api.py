# FreedomPay API Client
# Copyright (c) 2026, Viktor Krasnikov and contributors
# For license information, please see license.txt

import frappe
import requests
import hashlib
import random
import string
from urllib.parse import urlencode
from typing import Dict, Any, Optional

class FreedomPayAPI:
    """FreedomPay API Client for payment processing"""

    def __init__(self, merchant_id: str, secret_key: str, base_url: str = "https://api.freedompay.uz"):
        """
        Initialize FreedomPay API client

        Args:
            merchant_id (str): FreedomPay merchant ID
            secret_key (str): FreedomPay secret key
            base_url (str): FreedomPay API base URL
        """
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = base_url
        self.timeout = 30

    def create_payment(self, amount: str, currency: str, order_id: str, description: str, **kwargs) -> Dict[str, Any]:
        """
        Create payment request

        Args:
            amount (str): Payment amount
            currency (str): Payment currency (UZS, USD, etc.)
            order_id (str): Order ID
            description (str): Payment description
            **kwargs: Additional payment parameters

        Returns:
            Dict[str, Any]: Payment response data

        Raises:
            frappe.ValidationError: If payment creation fails
        """
        data = {
            'pg_merchant_id': self.merchant_id,
            'pg_amount': amount,
            'pg_currency': currency,
            'pg_order_id': order_id,
            'pg_description': description,
            **kwargs
        }

        # Generate signature
        signature = self._generate_signature(data, "init_payment.php")
        data['pg_sig'] = signature

        try:
            response = requests.post(
                f"{self.base_url}/init_payment.php",
                data=data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"FreedomPay API request failed: {str(e)}")
            frappe.throw(_("FreedomPay API connection error"))

    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Check payment status

        Args:
            payment_id (str): Payment ID to check

        Returns:
            Dict[str, Any]: Payment status data
        """
        data = {
            'pg_merchant_id': self.merchant_id,
            'pg_payment_id': payment_id,
        }

        signature = self._generate_signature(data, "get_status.php")
        data['pg_sig'] = signature

        try:
            response = requests.post(
                f"{self.base_url}/get_status.php",
                data=data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"FreedomPay status check failed: {str(e)}")
            frappe.throw(_("FreedomPay status check failed"))

    def create_payout(self, amount: str, currency: str, card_number: str, **kwargs) -> Dict[str, Any]:
        """
        Create payout request

        Args:
            amount (str): Payout amount
            currency (str): Payout currency
            card_number (str): Card number for payout
            **kwargs: Additional payout parameters

        Returns:
            Dict[str, Any]: Payout response data
        """
        data = {
            'pg_merchant_id': self.merchant_id,
            'pg_amount': amount,
            'pg_currency': currency,
            'pg_card_number': card_number,
            **kwargs
        }

        signature = self._generate_signature(data, "init_payout.php")
        data['pg_sig'] = signature

        try:
            response = requests.post(
                f"{self.base_url}/init_payout.php",
                data=data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"FreedomPay payout failed: {str(e)}")
            frappe.throw(_("FreedomPay payout failed"))

    def _generate_signature(self, data: Dict[str, Any], script_name: str) -> str:
        """
        Generate MD5 signature for FreedomPay API

        Args:
            data (Dict[str, Any]): Data to sign
            script_name (str): API script name

        Returns:
            str: MD5 signature
        """
        # Generate random salt
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        data['pg_salt'] = salt

        # Create signature string
        signature_string = f"{script_name};"
        for key in sorted(data.keys()):
            if key != 'pg_sig':
                signature_string += f"{key}={data[key]};"

        signature_string += self.secret_key

        return hashlib.md5(signature_string.encode('utf-8')).hexdigest()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response

        Args:
            response (requests.Response): API response

        Returns:
            Dict[str, Any]: Parsed response data

        Raises:
            frappe.ValidationError: If response indicates error
        """
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                # Parse as form data if not JSON
                form_data = {}
                for item in response.text.split('&'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        form_data[key] = value
                return form_data
        else:
            error_msg = response.text or _("Unknown error")
            frappe.log_error(f"FreedomPay API error: {response.status_code} - {error_msg}")
            frappe.throw(_("FreedomPay API error: {0}").format(error_msg))
