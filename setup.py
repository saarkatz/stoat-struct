from setuptools import setup, find_packages


setup(
    name="py-structure",
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
