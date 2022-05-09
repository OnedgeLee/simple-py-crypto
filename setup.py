from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycrypto",
    version="0.0.0",
    description="Simple crypto implementation with python",
    author="OnedgeLee",
    author_email="Onedge.Lee@gmail.com",
    url="https://github.com/OnedgeLee/simple-py-crypto",
    packages=find_packages()
)