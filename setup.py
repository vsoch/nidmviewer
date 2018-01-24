from setuptools import setup, find_packages
import codecs
import os

setup(
    # Application name:
    name="nidmviewer",

    # Version number (initial):
    version="0.1.4",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data
    package_data = {'nidmviewer.template':['*.html','*.zip','*.js','*.css'],
                    'nidmviewer.data':['*.nii.gz']},

    # Details
    url="http://www.github.com/vsoch/nidmviewer",

    license="LICENSE.txt",
    description="command line or server tool to view or compare nidm results.",
    keywords='nidm nidm-results brain imaging neuroimaging',

    # python -m pip install requirements.txt
    install_requires = ['numpy','rdflib','rdfextras','rdflib-jsonld','pandas', 'nibabel', 'pyparsing'],

    entry_points = {
        'console_scripts': [
            'nidmviewer=nidmviewer.scripts:main',
        ],
    },
)
