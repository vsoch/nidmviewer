#!/usr/bin/python

from nidmviewer.viewer import generate
from glob import glob
import os

# HTML FOR EMBEDDING #####################################################
# Here are images that we want to see, these should be relative to your web server
nidm_files = glob("fsl/*.ttl")
standard_brain = "fsl/MNI152_T1_2mm_brain.nii.gz"

# If no base_image is specified, the background will be black
html_snippet = generate(nidm_files=nidm_files,base_image=standard_brain)


# LOCAL BROWSER ##########################################################
# Here are images that we want to see, matches with nidm
nidm_files = [os.path.abspath(f) for f in glob("fsl/*.ttl")]
standard_brain = os.path.abspath("fsl/MNI152_T1_2mm_brain.nii.gz")

# You can generate something to view in your browser
# If no base_image is specified, the background will be black
httpd = generate(nidm_files=nidm_files,base_image=standard_brain,view_in_browser=True)

