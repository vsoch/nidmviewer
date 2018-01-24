#!/usr/bin/python

from nidmviewer.viewer import generate
from glob import glob
import os

# These examples are for generating code for the viewer from within python. You can achieve
# the local browser version by running from the command line:

# nidmviewer  fsl/nidm.ttl
# nidmviewer  fsl/nidm1.ttl,nidm2.ttl

# HTML FOR EMBEDDING #####################################################
# Here are images that we want to see, these should be relative to your web server
# Each ttl file must be matched with a provn file, in the case of different versions
ttl_files = glob("fsl/*.ttl")
html_snippet = generate(ttl_files=ttl_files)

# To make sure the html snippet is relative to the generation directory (e.g., add fsl/)
html_snippet = generate(ttl_files=ttl_files, relative_to='fsl/')

# You would then save this to file (or render into a template) and you are
# in charge of having the web server and favicon.ico :)
