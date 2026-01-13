# Copyright (c) 2026, Viktor Krasnikov and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class FreedomPaySettings(Document):
    def on_update(self):
        """Create payment gateway when settings are updated"""
        from payments.utils import create_payment_gateway
        create_payment_gateway(
            "FreedomPay-" + self.gateway_name,
            settings="FreedomPay Settings",
            controller=self.gateway_name,
        )
        if not self.flags.ignore_mandatory:
            self.validate_freedompay_credentials()

    def validate_freedompay_credentials(self):
        """Validate FreedomPay credentials"""
        if not self.merchant_id:
            frappe.throw(_("Merchant ID is required for FreedomPay"))

        if not self.get_password(fieldname="secret_key", raise_exception=False):
            frappe.throw(_("Secret Key is required for FreedomPay"))

    def validate_transaction_currency(self, currency):
        """Validate transaction currency"""
        # FreedomPay supports UZS and other currencies
        supported_currencies = ["UZS", "USD", "EUR", "RUB"]
        if currency not in supported_currencies:
            frappe.throw(
                _("FreedomPay does not support transactions in currency '{0}'").format(currency)
            )

    def get_payment_url(self, **kwargs):
        """Get payment URL for checkout"""
        from frappe.utils import get_url
        from urllib.parse import urlencode
        return get_url(f"./freedompay_checkout?{urlencode(kwargs)}")

    def create_request(self, data):
        """Create payment request"""
        from frappe.integrations.utils import create_request_log
        from .freedompay_api import FreedomPayAPI

        self.data = frappe._dict(data)

        try:
            self.integration_request = create_request_log(self.data, service_name="FreedomPay")
            return self.create_payment_on_freedompay()
        except Exception:
            frappe.log_error(frappe.get_traceback())
            return {
                "redirect_to": frappe.redirect_to_message(
                    _("Server Error"),
                    _("There was an issue with the FreedomPay configuration."),
                ),
                "status": 401,
            }

    def create_payment_on_freedompay(self):
        """Create payment on FreedomPay"""
        from .freedompay_api import FreedomPayAPI

        api = FreedomPayAPI()

        payment_data = {
            "amount": self.data.amount,
            "currency": self.data.currency or "UZS",
            "description": self.data.description or "",
            "order_id": self.data.reference_docname,
            "result_url": self.data.result_url,
            "success_url": self.data.success_url,
            "failure_url": self.data.failure_url,
            "check_url": self.data.check_url,
            "user_id": self.data.payer_email,
            "email": self.data.payer_email,
            "phone": self.data.payer_phone,
        }

        code, payment, feedback = api.create_payment(payment_data)

        if code == "SUCCESS":
            self.integration_request.db_set("status", "Completed", update_modified=False)
            self.flags.status_changed_to = "Completed"
        else:
            frappe.log_error(f"FreedomPay Payment Failed: {feedback.error}")
            self.integration_request.db_set("status", "Failed", update_modified=False)

        return self.finalize_request()

    def finalize_request(self):
        """Finalize payment request and return redirect"""
        redirect_to = self.data.get("redirect_to") or None
        redirect_message = self.data.get("redirect_message") or None
        status = self.integration_request.status

        if self.flags.status_changed_to == "Completed":
            if self.data.reference_doctype and self.data.reference_docname:
                custom_redirect_to = None
                try:
                    custom_redirect_to = frappe.get_doc(
                        self.data.reference_doctype, self.data.reference_docname
                    ).run_method("on_payment_authorized", self.flags.status_changed_to)
                except Exception:
                    frappe.log_error(frappe.get_traceback())

                if custom_redirect_to:
                    redirect_to = custom_redirect_to

                redirect_url = f"payment-success?doctype={self.data.reference_doctype}&docname={self.data.reference_docname}"

            if hasattr(self, 'redirect_url') and self.redirect_url:
                redirect_url = self.redirect_url
                redirect_to = None
        else:
            redirect_url = "payment-failed"

        if redirect_to and "?" in redirect_url:
            redirect_url += "&" + urlencode({"redirect_to": redirect_to})
        else:
            redirect_url += "?" + urlencode({"redirect_to": redirect_to})

        if redirect_message:
            redirect_url += "&" + urlencode({"redirect_message": redirect_message})

        return {"redirect_to": redirect_url, "status": status}
