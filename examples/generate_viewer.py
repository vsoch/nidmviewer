#!/usr/bin/python

from nidmviewer.viewer import generate
from glob import glob
import os

# These examples are for running the viewer from within python. You can achieve
# the local browser version by running from the command line:

# nidmviewer --ttl fsl/nidm.ttl
# nidmviewer --ttl fsl/nidm1.ttl,nidm2.ttl

# HTML FOR EMBEDDING #####################################################
# Here are images that we want to see, these should be relative to your web server
# Each ttl file must be matched with a provn file, in the case of different versions
ttl_files = glob("fsl/*.ttl")
standard_brain = "fsl/MNI152_T1_2mm_brain.nii.gz"

# By default, all columns that are possible (based on data in the ttl) are generated.
# Specify a set to remove from each:
columns_to_remove = ['type', 'atLocation', 'wasDerivedFrom', 'value', 'coordinateVector']

# If no base_image is specified, the background will be black
html_snippet = generate(ttl_files=ttl_files,
                        base_image=standard_brain,
                        columns_to_remove=columns_to_remove)


# LOCAL BROWSER ##########################################################
# Here are images that we want to see, matches with nidm
nidm_files = [os.path.abspath(f) for f in glob("fsl/*.ttl")]
standard_brain = os.path.abspath("fsl/MNI152_T1_2mm_brain.nii.gz")

# You can generate something to view in your browser
# If no base_image is specified, the background will be black
httpd = generate(ttl_files=nidm_files,base_image=standard_brain,view_in_browser=True)
