# Copyright (c) 2026, Viktor Krasnikov and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.integrations.utils import create_request_log

from .freedompay_api import FreedomPayAPI


def create_freedompay_payment(gateway_controller, data):
    settings = frappe.get_doc("FreedomPay Settings")
    settings.data = frappe._dict(data)

    api = FreedomPayAPI()
    settings.integration_request = create_request_log(settings.data, "Host", "FreedomPay")

    try:
        payment_data = {
            "amount": settings.data.amount,
            "currency": settings.data.currency or "UZS",
            "description": settings.data.description or "",
            "order_id": settings.data.reference_docname,
            "result_url": settings.data.result_url,
            "success_url": settings.data.success_url,
            "failure_url": settings.data.failure_url,
            "check_url": settings.data.check_url,
            "user_id": settings.data.payer_email,
            "email": settings.data.payer_email,
            "phone": settings.data.payer_phone,
        }

        code, payment, feedback = api.create_payment(payment_data)

        if code == "SUCCESS":
            settings.integration_request.db_set("status", "Completed", update_modified=False)
            settings.flags.status_changed_to = "Completed"

            # Return redirect URL from payment response
            redirect_url = payment.get("pg_redirect_url") or payment.get("redirect_url")
            if redirect_url:
                return {
                    "redirect_to": redirect_url,
                    "status": "Completed",
                }
            else:
                # If no redirect URL, payment might be processed immediately
                return {
                    "redirect_to": frappe.redirect_to_message(
                        _("Payment Completed"),
                        _("Your payment has been processed successfully."),
                    ),
                    "status": "Completed",
                }
        else:
            settings.integration_request.db_set("status", "Failed", update_modified=False)
            frappe.log_error(f"FreedomPay Payment Failed: {feedback.error}")
            return {
                "redirect_to": frappe.redirect_to_message(
                    _("Payment Failed"),
                    _(f"Payment could not be processed: {feedback.error}"),
                ),
                "status": "Failed",
            }

    except Exception as e:
        settings.integration_request.db_set("status", "Failed", update_modified=False)
        settings.log_error(f"FreedomPay Payment Error: {str(e)}")
        return {
            "redirect_to": frappe.redirect_to_message(
                _("Server Error"),
                _("There was an issue processing the payment. Please try again."),
            ),
            "status": "Failed",
        }


def verify_freedompay_payment(payment_id):
    """Verify payment status from FreedomPay callback"""
    api = FreedomPayAPI()
    code, status, feedback = api.check_payment_status(payment_id)

    if code == "SUCCESS":
        return status
    else:
        frappe.log_error(f"FreedomPay Status Check Failed: {feedback.error}")
        return None


def create_freedompay_payout(data):
    """Create payout through FreedomPay"""
    api = FreedomPayAPI()
    code, payout, feedback = api.create_payout(data)

    if code == "SUCCESS":
        return payout
    else:
        frappe.log_error(f"FreedomPay Payout Failed: {feedback.error}")
        return None
