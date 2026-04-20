from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Study Buddy",
    version="0.1.0",
    packages=find_packages(),
    author="Dhivya",
    install_requires=requirements,
)