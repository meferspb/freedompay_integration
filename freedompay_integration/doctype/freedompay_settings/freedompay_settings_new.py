# FreedomPay Settings
# Copyright (c) 2026, Viktor Krasnikov and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from payments.utils import create_payment_gateway
from typing import Optional

class FreedomPaySettings(Document):
    """FreedomPay Settings Document"""

    def on_update(self) -> None:
        """Create payment gateway when settings are updated"""
        try:
            create_payment_gateway(
                "FreedomPay",
                settings="FreedomPay Settings",
                controller=self.name
            )
            frappe.msgprint(_("FreedomPay Payment Gateway created successfully"))
        except Exception as e:
            frappe.log_error(f"Error creating payment gateway: {str(e)}")
            frappe.msgprint(_("Could not create payment gateway: {0}").format(str(e)))

    def validate(self) -> None:
        """Validate settings before saving"""
        self._validate_required_fields()
        self._validate_urls()

    def _validate_required_fields(self) -> None:
        """Validate required fields"""
        if not self.merchant_id:
            frappe.throw(_("Merchant ID is required"))

        if not self.get_password("secret_key"):
            frappe.throw(_("Secret Key is required"))

    def _validate_urls(self) -> None:
        """Validate URL fields"""
        if not self.result_url:
            frappe.throw(_("Result URL is required"))

        if not self.success_url:
            frappe.throw(_("Success URL is required"))

        if not self.failure_url:
            frappe.throw(_("Failure URL is required"))

    def validate_transaction_currency(self, currency: str) -> None:
        """Validate transaction currency"""
        supported_currencies = ["UZS", "USD", "EUR", "RUB"]
        if currency not in supported_currencies:
            frappe.throw(
                _("FreedomPay does not support transactions in currency '{0}'").format(currency)
            )

    def get_payment_url(self, **kwargs) -> str:
        """Get payment URL for checkout"""
        from frappe.utils import get_url
        from urllib.parse import urlencode
        return get_url(f"./freedompay_checkout?{urlencode(kwargs)}")

    def create_request(self, data: dict) -> dict:
        """Create payment request"""
        from frappe.integrations.utils import create_request_log

        self.data = frappe._dict(data)

        try:
            self.integration_request = create_request_log(
                self.data,
                service_name="FreedomPay",
                reference_doctype=self.data.reference_doctype,
                reference_docname=self.data.reference_docname
            )

            return self._create_payment_on_freedompay()

        except Exception as e:
            frappe.log_error(frappe.get_traceback())
            return {
                "redirect_to": frappe.redirect_to_message(
                    _("Server Error"),
                    _("There was an issue with the FreedomPay configuration."),
                ),
                "status": 401,
            }

    def _create_payment_on_freedompay(self) -> dict:
        """Create payment on FreedomPay"""
        from freedompay_integration.payment_gateway import create_payment

        try:
            result = create_payment(self.name, self.data)

            if result.get("status") == "Completed":
                self.integration_request.db_set("status", "Completed", update_modified=False)
                return result
            else:
                self.integration_request.db_set("status", "Failed", update_modified=False)
                frappe.log_error(f"FreedomPay payment failed")
                return {
                    "redirect_to": frappe.redirect_to_message(
                        _("Payment Failed"),
                        _("Payment could not be processed."),
                    ),
                    "status": "Failed",
                }

        except Exception as e:
            self.integration_request.db_set("status", "Failed", update_modified=False)
            frappe.log_error(f"FreedomPay payment error: {str(e)}")
            return {
                "redirect_to": frappe.redirect_to_message(
                    _("Server Error"),
                    _("There was an issue processing the payment."),
                ),
                "status": "Failed",
            }
