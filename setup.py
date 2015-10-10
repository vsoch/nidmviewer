from setuptools import setup, find_packages

setup(
    # Application name:
    name="nidmviewer",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data
    package_data = {'nidmviewer.template':['*.html','*.zip','*.js','*.css']},

    # Details
    url="http://www.github.com/vsoch/nidmviewer",

    license="LICENSE.txt",
    description="command line or server tool to view or compare nidm results.",

    install_requires = ['numpy','rdflib']
)
