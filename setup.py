from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from requirements.txt file
reqs = [line.strip() for line in open('requirements.txt').readlines()]
requirements = list(filter(None, reqs))

setup(
    # Application name:
    name="nidmviewer",

    # Version number (initial):
    version="0.1.1",

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
    long_description=long_description,
    keywords='nidm nidm-results brain imaging neuroimaging',

    install_requires = requirements,

    entry_points = {
        'console_scripts': [
            'nidmviewer=nidmviewer.scripts:main',
        ],
    },
)
