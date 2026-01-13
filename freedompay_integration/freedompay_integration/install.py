import frappe

def before_install():
    pass

def after_install():
    # Create default FreedomPay Settings if it doesn't exist
    if not frappe.db.exists("DocType", "FreedomPay Settings"):
        frappe.reload_doc("freedompay_integration", "doctype", "freedompay_settings")
        frappe.db.commit()

    # Create default settings record
    if not frappe.db.exists("FreedomPay Settings", "FreedomPay Settings"):
        settings = frappe.new_doc("FreedomPay Settings")
        settings.save()
        frappe.db.commit()
