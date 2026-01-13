#!/usr/bin/env python3
"""
Test script to verify that the FreedomPay Integration app builds correctly
without frontend assets.
"""

import json
import subprocess
import sys
import os

def test_build_configuration():
    """Test that build configuration is correct"""
    print("Testing build configuration...")

    # Check build.json
    with open('build.json', 'r') as f:
        build_config = json.load(f)

    assert build_config['build'] == False, "Build should be disabled"
    assert build_config['assets'] == [], "Assets should be empty"
    assert build_config['apps'] == [], "Apps list should be empty"

    print("✓ Build configuration is correct")

def test_package_json():
    """Test that package.json has proper build scripts"""
    print("Testing package.json...")

    with open('package.json', 'r') as f:
        package_config = json.load(f)

    assert 'production' in package_config['scripts'], "Production script should exist"
    assert 'build' in package_config['scripts'], "Build script should exist"

    print("✓ Package.json configuration is correct")

def test_yarn_production():
    """Test that yarn production command works"""
    print("Testing yarn production command...")

    try:
        result = subprocess.run(['yarn', 'run', 'production'],
                              capture_output=True, text=True, check=True)
        print(f"✓ Yarn production command succeeded: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Yarn production command failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠ Yarn not found, skipping yarn test")
        return True

    return True

def main():
    """Run all tests"""
    print("Running FreedomPay Integration build tests...\n")

    try:
        test_build_configuration()
        test_package_json()

        if not test_yarn_production():
            return 1

        print("\n✓ All tests passed! The app should build successfully.")
        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
