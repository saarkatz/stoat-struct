from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stoat",
    version="0.0.1",
    author="Saar Katz",
    author_email="kats.saar@gmail.com",
    description="A package for declarative definition of binary structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saarkatz/stoat-struct",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
