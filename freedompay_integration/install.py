import frappe
import os
import subprocess

def before_install():
    """Check if app is in apps.txt and add if not"""
    try:
        # Get bench directory path
        bench_dir = frappe.get_app_path("frappe").replace("/apps/frappe", "")

        apps_txt_path = os.path.join(bench_dir, "apps.txt")

        # Check if app is already in apps.txt
        if os.path.exists(apps_txt_path):
            with open(apps_txt_path, 'r') as f:
                apps = f.read().splitlines()

            if "freedompay_integration" not in apps:
                # Add app to apps.txt
                with open(apps_txt_path, 'a') as f:
                    f.write("freedompay_integration\n")

                frappe.msgprint(
                    "FreedomPay Integration added to apps.txt automatically.",
                    alert=True
                )
        else:
            frappe.msgprint(
                "apps.txt not found. Please manually add freedompay_integration to apps.txt",
                alert=True
            )
    except Exception as e:
        frappe.log_error(f"Error in before_install: {str(e)}")
        frappe.msgprint(
            f"Could not automatically add to apps.txt: {str(e)}. Please manually add freedompay_integration to apps.txt",
            alert=True
        )

def after_install():
    """Create default FreedomPay Settings and Payment Gateway"""
    # Create default FreedomPay Settings if it doesn't exist
    if not frappe.db.exists("DocType", "FreedomPay Settings"):
        frappe.reload_doc("freedompay_integration", "doctype", "freedompay_settings")
        frappe.db.commit()

    # Create default settings record
    if not frappe.db.exists("FreedomPay Settings", "FreedomPay Settings"):
        settings = frappe.new_doc("FreedomPay Settings")
        settings.save()
        frappe.db.commit()

    # Create Payment Gateway if payments app is installed
    try:
        if "payments" in frappe.get_installed_apps():
            from payments.utils import create_payment_gateway
            create_payment_gateway(
                "FreedomPay",
                settings="FreedomPay Settings",
                controller="FreedomPay Settings"
            )
            frappe.msgprint(
                "FreedomPay Payment Gateway created successfully!",
                alert=True
            )
        else:
            frappe.msgprint(
                "Payments app not installed. FreedomPay Payment Gateway not created.",
                alert=True
            )
    except Exception as e:
        frappe.log_error(f"Error creating payment gateway: {str(e)}")
        frappe.msgprint(
            f"Could not create payment gateway: {str(e)}",
            alert=True
        )
