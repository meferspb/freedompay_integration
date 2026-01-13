import hashlib
import random
import string
import json

import frappe
import requests

from .response_feedback import ResponseFeedBack


class FreedomPayConnection:
    def __init__(self):
        self.settings = frappe.get_doc("FreedomPay Settings")

    def post(self, url, data=None, use_form_data=True):
        """POST request with signature"""
        try:
            if use_form_data and data:
                # Generate signature for form data
                signature = self.generate_signature(url, data)
                data['pg_sig'] = signature

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded' if use_form_data else 'application/json'
            }

            if use_form_data:
                response = requests.post(url, data=data, headers=headers, timeout=30)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=30)

            return self._handle_response(response)
        except Exception as e:
            return "ERROR", ResponseFeedBack(error=str(e))

    def get(self, url, params=None):
        """GET request with signature"""
        try:
            if params:
                signature = self.generate_signature(url, params)
                params['pg_sig'] = signature

            response = requests.get(url, params=params, timeout=30)
            return self._handle_response(response)
        except Exception as e:
            return "ERROR", ResponseFeedBack(error=str(e))

    def generate_signature(self, url, data):
        """Generate MD5 signature according to FreedomPay documentation"""
        # Extract script name from URL (from last / to end or ?)
        script_name = url.split('/')[-1].split('?')[0]

        # Generate random salt
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        data['pg_salt'] = salt

        # Sort fields alphabetically
        sorted_keys = sorted(data.keys())

        # Concatenate: script_name;field1=value1;field2=value2;...;pg_salt=salt_value;secret_key
        signature_string = script_name + ';'
        for key in sorted_keys:
            if key != 'pg_sig':  # Don't include signature in signature calculation
                signature_string += f"{key}={data[key]};"

        # Add secret key
        signature_string += self.settings.get_password('secret_key')

        # Calculate MD5
        return hashlib.md5(signature_string.encode('utf-8')).hexdigest()

    def _handle_response(self, response):
        """Handle API response"""
        try:
            if response.status_code == 200:
                # Try to parse as JSON first, then as form data
                try:
                    data = response.json()
                    return "SUCCESS", ResponseFeedBack(data=data)
                except json.JSONDecodeError:
                    # Parse as form data
                    data = {}
                    for item in response.text.split('&'):
                        if '=' in item:
                            key, value = item.split('=', 1)
                            data[key] = value
                    return "SUCCESS", ResponseFeedBack(data=data)
            else:
                try:
                    data = response.json()
                    error_msg = data.get("pg_error_description", data.get("message", "Unknown error"))
                except:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                return "FAILED", ResponseFeedBack(error=error_msg)
        except Exception as e:
            return "ERROR", ResponseFeedBack(error=str(e))
