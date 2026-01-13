from typing import Any, Union

import frappe

from .connection import FreedomPayConnection
from .urls import FreedomPayUrls
from .response_codes import SUCCESS
from .response_feedback import ResponseFeedBack


class FreedomPayAPI:
    def __init__(self) -> None:
        """Class for FreedomPay APIs"""
        self.connection = FreedomPayConnection()
        self.settings = frappe.get_doc("FreedomPay Settings")
        self.urls = FreedomPayUrls()

    def create_payment(self, data: dict) -> tuple[str, dict | None, ResponseFeedBack]:
        """
        Creates a FreedomPay Payment
        :param data: Dictionary containing payment details
        :return: Tuple[str, Union[Dict, None], ResponseFeedBack]
        """
        # Prepare payment data according to FreedomPay API
        payment_data = {
            'pg_merchant_id': self.settings.merchant_id,
            'pg_amount': data.get('amount'),
            'pg_currency': data.get('currency', 'UZS'),
            'pg_description': data.get('description', ''),
        }

        # Add URL fields with validation
        result_url = self.settings.result_url or data.get('result_url')
        success_url = self.settings.success_url or data.get('success_url')
        failure_url = self.settings.failure_url or data.get('failure_url')
        check_url = self.settings.check_url or data.get('check_url')

        if not result_url:
            frappe.throw("Result URL is required for FreedomPay payment. Please configure it in FreedomPay Settings or provide it in the payment data.")

        payment_data['pg_result_url'] = result_url

        if success_url:
            payment_data['pg_success_url'] = success_url
        if failure_url:
            payment_data['pg_failure_url'] = failure_url
        if check_url:
            payment_data['pg_check_url'] = check_url

        # Add optional fields
        if data.get('order_id'):
            payment_data['pg_order_id'] = data.get('order_id')
        if data.get('user_id'):
            payment_data['pg_user_id'] = data.get('user_id')
        if data.get('email'):
            payment_data['pg_user_email'] = data.get('email')
        if data.get('phone'):
            payment_data['pg_user_phone'] = data.get('phone')

        code, feedback = self.connection.post(
            url=self.urls.create_payment(), data=payment_data
        )

        payment = frappe._dict()

        if code == SUCCESS:
            payment = feedback.data
            feedback.message = "Payment Created Successfully"

        return code, payment, feedback

    def check_payment_status(self, payment_id: str) -> tuple[str, dict | None, ResponseFeedBack]:
        """Checks Payment Status by Payment ID

        Args:
            payment_id (str): FreedomPay Payment ID

        Returns:
            Tuple[str, Union[Dict, None], ResponseFeedBack]
        """
        status_data = {
            'pg_merchant_id': self.settings.merchant_id,
            'pg_payment_id': payment_id,
        }

        code, feedback = self.connection.post(
            url=self.urls.payment_status(), data=status_data
        )
        status = None
        if code == SUCCESS:
            status = feedback.data
            feedback.message = f"Payment status for {payment_id} retrieved successfully"
        return code, status, feedback

    def create_payout(self, data: dict) -> tuple[str, dict | None, ResponseFeedBack]:
        """
        Creates a FreedomPay Payout
        :param data: Dictionary containing payout details
        :return: Tuple[str, Union[Dict, None], ResponseFeedBack]
        """
        payout_data = {
            'pg_merchant_id': self.settings.merchant_id,
            'pg_amount': data.get('amount'),
            'pg_currency': data.get('currency', 'UZS'),
            'pg_card_number': data.get('card_number'),
            'pg_cardholder_name': data.get('cardholder_name'),
            'pg_post_link': self.settings.post_link or data.get('post_link'),
        }

        # Use payout secret key if available
        if self.settings.get_password('secret_key_payout'):
            # Create a temporary settings object with payout key
            payout_key = self.settings.get_password('secret_key_payout')

            # Create a mock settings object that returns payout key for get_password('secret_key')
            class PayoutSettings:
                def __init__(self, original_settings, payout_key):
                    self.original_settings = original_settings
                    self.payout_key = payout_key

                def get_password(self, field_name):
                    if field_name == 'secret_key':
                        return self.payout_key
                    return self.original_settings.get_password(field_name)

                def __getattr__(self, name):
                    return getattr(self.original_settings, name)

            # Create temporary connection with payout settings
            temp_connection = FreedomPayConnection()
            temp_connection.settings = PayoutSettings(self.settings, payout_key)

            code, feedback = temp_connection.post(
                url=self.urls.create_payout(), data=payout_data
            )
        else:
            code, feedback = self.connection.post(
                url=self.urls.create_payout(), data=payout_data
            )

        payout = frappe._dict()

        if code == SUCCESS:
            payout = feedback.data
            feedback.message = "Payout Created Successfully"

        return code, payout, feedback
