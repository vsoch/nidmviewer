'''

Copyright (c) 2005-2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the NumPy Developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import contextlib
import tempfile
import nibabel
import zipfile
import shutil
import string
import numpy
import random
import os
import re
import sys

# Imports based on python 2 and 3
try:
    from urllib.request import urlopen
except:
    from urllib2 import urlopen

# Get the directory of the package
def get_package_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Make directory
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Make temporary directory
@contextlib.contextmanager
def make_tmp_folder():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

# Reading Files
def read_file_lines(file_name):
    filey = open(file_name,'r')
    file_contents = filey.readlines()
    filey.close()
    return file_contents


def download_file(src, dest=None, download_folder=None):
    '''download file will return a downloaded temporary path specified, or
       if not possible, return the original source path with a warning.
 
       Parameters
       ==========
       src: the source path to download
       dest: the destination path to download to. If not set, creates temporary
             directory. The user can either provide a complete destination path,
             (dest) or a download folder (and have a dest generated with it)

    '''

    # if the dest not provided, return randomly generated based on folder
    if dest is None:
        dest = get_tmpname(src, download_folder)

    try:
        if sys.version_info < (3,):
            import urllib
            requester = urllib.FancyURLopener()
            requester.retrieve(src, dest)
        else:
            import urllib.request
            opener = urllib.request.urlopen(src)
            with open(dest, 'wb') as fp:
                fp.write(opener.read())
        return dest
    except:
        print("Cannot download %s" %src)
        return src


def get_redirect_url(url):
    '''follow a redirect with a FancyUrlOpener. If it's not a url,
       we pass and return the original file path.

       Parameters
       ==========
       url: the path or url to follow

    '''

    # Local file doesn't have redirect
    if url.startswith('file://'):
        return re.sub('^file://','', url)
    try:
        url = urlopen(url).url
    except:
        pass
    return url

    
# Filenames
def get_tmpname(brainmap, temp_dir=None):
    '''get tmpname will return a temporary file name based on an input (likely
       nifti) file.

       Parameters
       ==========
       brainmap: the path to the brainmap
       temp_dir: a path to a temporary directory to use. If not defined,
                 one is created on the fly.

    '''
    image_ext = get_extension(brainmap)
    temp_path = get_random_name()

    # If temporary directory not defined, create!
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()

    return "%s/%s.%s" %(temp_dir,temp_path,image_ext)


def get_random_name(length=6,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))


def get_extension(path):
    fileparts =  os.path.basename(path).split(".")
    fileparts.pop(0)
    return ".".join(fileparts)


# Brain image templates
def get_standard_brain():
    return "https://rawgit.com/vsoch/nidmviewer/master/nidmviewer/data/MNI152_T1_2mm_brain.nii.gz"


# Check if nifti is empty
def _is_empty(nii_file):
    '''driver function to determine if single nifti file is empty
    '''
    nii = nibabel.load(nii_file)
    data = nii.get_data()
    data = numpy.nan_to_num(data)
    if numpy.count_nonzero(data) == 0:
        return 1
    return 0


def is_empty(peaks, check_empty=True, location_key='excsetmap_location'):
    '''find empty will take a peaks lookup in form {nidm: {name: brainmap }}
       and return a lookup dictionary with 0 if a brainmap is empty, 1 if not

       Parameters
       ==========
       lookup: dictionary of nidm files, names, and brainmaps in format
                form {nidm: {name: brainmap }}
       check_empty: a 0/1 to distinguish empty (1) or not (0)

    '''
    empty_images = dict()

    for nidm, items in peaks.items():
        for item in items:
            status = 0
            image_file = item[location_key]
            if os.path.exists(image_file):
                # Generate a lookup with 1 if empty, 0f not
                if check_empty is True and image_file not in empty_images:
                    status = _is_empty(image_file)

            empty_images[image_file] = status

    return empty_images
