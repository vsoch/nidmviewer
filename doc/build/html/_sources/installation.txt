Installation
============

To install

::


      pip install git+git://github.com/vsoch/nidmviewer.git


Running Examples
----------------

Python (server)
'''''''''''''''

::

      #!/usr/bin/python

      from nidmviewer.viewer import generate
      from glob import glob
      import os

      # HTML FOR EMBEDDING #####################################################
      ttl_files = glob("fsl/*.ttl")
      html_snippet = generate(ttl_files=ttl_files)

      # LOCAL BROWSER ##########################################################
      httpd = generate(ttl_files=nidm_files,base_image=standard_brain,view_in_browser=True)


Command Line
''''''''''''

When installing with setup.py, an executable, `nidmviewer` is installed in your bin to view nidm files on the fly:

::

       nidmviewer fsl/nidm.ttl


You can see the basic usage by typing the command:


::

         nidmviewer 
          
         usage: nidmviewer [-h] [--columns_to_remove COLUMNS_TO_REMOVE] ttl base
         nidmviewer: error: too few arguments
         usage: nidmviewer [-h] [--columns_to_remove COLUMNS_TO_REMOVE] ttl base

         command line or server tool to view or compare nidm results.

         positional arguments:
           
             ttl                   List of comma separated ttl files to parse.
             base                  base image (standard brain map) to use for the viewer
                                   background.

