class FreedomPayUrls:
    def __init__(self):
        self.settings = frappe.get_doc("FreedomPay Settings")

    def create_payment(self):
        return f"{self.settings.base_url}/init_payment.php"

    def payment_status(self):
        return f"{self.settings.base_url}/get_status.php"

    def create_payout(self):
        return f"{self.settings.base_url}/init_payout.php"

    def refund_payment(self, payment_id):
        return f"{self.settings.base_url}/refund.php"
