#!/usr/bin/env python
from setuptools import setup, find_packages
import subprocess

def format_version():
    return subprocess.check_output(["git", "log", "-1", "--date=format:%Y%m%d.%H%M%S", "--format=git%cd-%h"])

setup(
    name = "qfil-unsparse",
    version = format_version(),
    packages = find_packages(),
    url = "https://github.com/NHellFire/android-qfil-unsparse",
    scripts = ["qfil-unsparse"]
    )

