# Frappe build configuration for FreedomPay Integration
# This app has no frontend assets, so skip the build process

def get_build_config():
    """Return build configuration for this app"""
    return {
        "build": False,  # Skip build process entirely
        "assets": [],    # No assets to build
    }

def get_build_hooks():
    """Return build hooks for this app"""
    return {
        "before_build": None,
        "after_build": None,
    }
