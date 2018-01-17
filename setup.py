from setuptools import setup, find_packages
import codecs
import os

setup(
    # Application name:
    name="nidmviewer",

    # Version number (initial):
    version="0.1.3",

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

    install_requires = ['numpy','rdflib','rdfextras','rdflib-jsonld','pandas', 'nibabel', 'pyparsing==1.5.7','requests'],

    entry_points = {
        'console_scripts': [
            'nidmviewer=nidmviewer.scripts:main',
        ],
    },
)
