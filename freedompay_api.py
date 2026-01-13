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
            'pg_result_url': self.settings.result_url or data.get('result_url'),
            'pg_success_url': self.settings.success_url or data.get('success_url'),
            'pg_failure_url': self.settings.failure_url or data.get('failure_url'),
            'pg_check_url': self.settings.check_url or data.get('check_url'),
        }

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
            # Temporarily switch to payout secret key
            original_key = self.settings.get_password('secret_key')
            self.settings.secret_key = self.settings.get_password('secret_key_payout')

            code, feedback = self.connection.post(
                url=self.urls.create_payout(), data=payout_data
            )

            # Restore original key
            self.settings.secret_key = original_key
        else:
            code, feedback = self.connection.post(
                url=self.urls.create_payout(), data=payout_data
            )

        payout = frappe._dict()

        if code == SUCCESS:
            payout = feedback.data
            feedback.message = "Payout Created Successfully"

        return code, payout, feedback
