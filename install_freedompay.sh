#!/bin/bash

# FreedomPay Integration Installation Script
# This script automates the installation of FreedomPay Integration

# Check if we're in a bench directory
if [ ! -f "apps.txt" ]; then
    echo "Error: This script must be run from a Frappe bench directory"
    echo "Please cd to your frappe-bench directory first"
    echo "Example: cd /opt/frappe-server/frappe-bench"
    exit 1
fi

# Check if bench command is available
if ! command -v bench &> /dev/null; then
    echo "Error: bench command not found"
    echo "Make sure you're in a Frappe bench environment"
    exit 1
fi

# Check if site is specified
if [ -z "$1" ]; then
    echo "Usage: $0 <site-name>"
    echo "Example: $0 erp.local"
    exit 1
fi

SITE=$1

echo "=== FreedomPay Integration Installation ==="
echo "Site: $SITE"
echo ""

# Check if app is already in apps.txt
if grep -q "freedompay_integration" apps.txt; then
    echo "✓ FreedomPay Integration is already in apps.txt"
else
    echo "Adding freedompay_integration to apps.txt"
    echo "freedompay_integration" >> apps.txt
    echo "✓ Added freedompay_integration to apps.txt"
fi

# Check if app directory exists
if [ -d "apps/freedompay_integration" ]; then
    echo "✓ FreedomPay Integration app directory exists"
else
    echo "Error: FreedomPay Integration app directory not found"
    echo "Please run: bench get-app https://github.com/meferspb/freedompay_integration.git"
    exit 1
fi

echo ""
echo "Installing FreedomPay Integration for site $SITE..."
echo ""

# Install the app
bench --site $SITE install-app freedompay_integration

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 FreedomPay Integration installed successfully!"
    echo ""
    echo "=== Next Steps ==="
    echo "1. Go to Frappe Desktop"
    echo "2. Open FreedomPay Settings"
    echo "3. Configure required settings:"
    echo "   - Merchant ID (from FreedomPay)"
    echo "   - Secret Key (from FreedomPay)"
    echo "   - Result URL (your callback URL)"
    echo "   - Success URL (where to redirect after success)"
    echo "   - Failure URL (where to redirect after failure)"
    echo ""
    echo "4. Restart bench (optional):"
    echo "   bench restart"
    echo ""
    echo "5. Test the integration with a small payment"
    echo ""
else
    echo ""
    echo "❌ Error installing FreedomPay Integration"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check if payments app is installed: bench list-apps"
    echo "2. Check bench logs: bench logs"
    echo "3. Make sure you have all required dependencies"
    echo "4. Check file permissions: ls -la apps.txt"
    echo ""
    exit 1
fi
