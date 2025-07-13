#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="getmethatdawg-sdk",
    version="0.0.2",
    description="Zero-config deploy SDK for Python agents",
    author="GetMeThatDawg Team",
    author_email="hello@getmethatdawg.dev",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "gunicorn>=20.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 