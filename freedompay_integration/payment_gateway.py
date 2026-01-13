# FreedomPay Payment Gateway Integration
# Copyright (c) 2026, Viktor Krasnikov and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.integrations.utils import create_request_log
from freedompay.api import FreedomPayAPI
from typing import Dict, Any, Optional

def create_payment(gateway_controller: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create FreedomPay payment

    Args:
        gateway_controller (str): Gateway controller name
        data (Dict[str, Any]): Payment data

    Returns:
        Dict[str, Any]: Payment result with redirect URL

    Raises:
        frappe.ValidationError: If payment creation fails
    """
    # Get settings
    settings = frappe.get_doc("FreedomPay Settings", gateway_controller)

    # Validate settings
    _validate_settings(settings)

    # Initialize API client
    api = FreedomPayAPI(
        merchant_id=settings.merchant_id,
        secret_key=settings.get_password("secret_key"),
        base_url=settings.base_url or "https://api.freedompay.uz"
    )

    # Prepare payment data
    payment_data = {
        "amount": str(data.amount),
        "currency": data.currency or "UZS",
        "order_id": data.reference_docname,
        "description": data.description or _("Payment for {0}").format(data.reference_docname),
        "result_url": settings.result_url,
        "success_url": settings.success_url,
        "failure_url": settings.failure_url,
        "user_id": data.payer_email,
        "email": data.payer_email,
        "phone": data.payer_phone,
    }

    # Add optional fields
    if data.get("check_url"):
        payment_data["check_url"] = data.get("check_url")

    try:
        # Create request log
        settings.integration_request = create_request_log(
            data,
            service_name="FreedomPay",
            reference_doctype=data.reference_doctype,
            reference_docname=data.reference_docname
        )

        # Call FreedomPay API
        response = api.create_payment(**payment_data)

        # Handle response
        if response.get("pg_status") == "success":
            # Update request log
            settings.integration_request.db_set("status", "Completed", update_modified=False)

            return {
                "redirect_to": response.get("pg_redirect_url") or response.get("redirect_url"),
                "status": "Completed"
            }
        else:
            # Update request log
            settings.integration_request.db_set("status", "Failed", update_modified=False)
            frappe.log_error(f"FreedomPay payment failed: {response.get('pg_error_description')}")

            frappe.throw(_("Payment failed: {0}").format(response.get("pg_error_description", _("Unknown error"))))

    except Exception as e:
        # Update request log if exists
        if hasattr(settings, "integration_request"):
            settings.integration_request.db_set("status", "Failed", update_modified=False)

        frappe.log_error(f"FreedomPay payment error: {str(e)}")
        frappe.throw(_("Payment processing error: {0}").format(str(e)))

def verify_payment(payment_id: str) -> Optional[Dict[str, Any]]:
    """
    Verify FreedomPay payment status

    Args:
        payment_id (str): Payment ID to verify

    Returns:
        Optional[Dict[str, Any]]: Payment status data or None if failed
    """
    # Get settings
    settings = frappe.get_doc("FreedomPay Settings", "FreedomPay Settings")

    try:
        api = FreedomPayAPI(
            merchant_id=settings.merchant_id,
            secret_key=settings.get_password("secret_key")
        )

        response = api.check_payment_status(payment_id)

        if response.get("pg_status") == "success":
            return response
        else:
            frappe.log_error(f"FreedomPay verification failed: {response.get('pg_error_description')}")
            return None

    except Exception as e:
        frappe.log_error(f"FreedomPay verification error: {str(e)}")
        return None

def create_payout(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Create FreedomPay payout

    Args:
        data (Dict[str, Any]): Payout data

    Returns:
        Optional[Dict[str, Any]]: Payout result or None if failed
    """
    settings = frappe.get_doc("FreedomPay Settings", "FreedomPay Settings")

    try:
        api = FreedomPayAPI(
            merchant_id=settings.merchant_id,
            secret_key=settings.get_password("secret_key")
        )

        payout_data = {
            "amount": str(data.amount),
            "currency": data.currency or "UZS",
            "card_number": data.card_number,
            "cardholder_name": data.cardholder_name,
        }

        if data.get("post_link"):
            payout_data["post_link"] = data.get("post_link")

        response = api.create_payout(**payout_data)

        if response.get("pg_status") == "success":
            return response
        else:
            frappe.log_error(f"FreedomPay payout failed: {response.get('pg_error_description')}")
            return None

    except Exception as e:
        frappe.log_error(f"FreedomPay payout error: {str(e)}")
        return None

def _validate_settings(settings: "FreedomPaySettings") -> None:
    """
    Validate FreedomPay settings

    Args:
        settings (FreedomPaySettings): Settings to validate

    Raises:
        frappe.ValidationError: If settings are invalid
    """
    if not settings.merchant_id:
        frappe.throw(_("FreedomPay Merchant ID is not configured"))

    if not settings.get_password("secret_key"):
        frappe.throw(_("FreedomPay Secret Key is not configured"))

    if not settings.result_url:
        frappe.throw(_("FreedomPay Result URL is not configured"))

    if not settings.success_url:
        frappe.throw(_("FreedomPay Success URL is not configured"))

    if not settings.failure_url:
        frappe.throw(_("FreedomPay Failure URL is not configured"))
