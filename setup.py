"""
Setup for FreedomPay Integration
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="freedompay_integration",
    version="1.0.0",
    description="FreedomPay payment gateway integration for Frappe",
    author="Viktor Krasnikov",
    author_email="vmk1981rus@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
