'''
utils.py: part of the nidmviewer package
Functions to work with html templates

'''

import numpy as np
import contextlib
import tempfile
import nibabel
import zipfile
import urllib
import shutil
import string
import numpy
import random
import os


# Split a url to just get base
def strip_url(url,encode=True):
    if encode:
        return url.split("/")[-1].encode("utf-8")
    else:
        return url.split("/")[-1]

# Get the directory of the package
def get_package_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Make directory
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Unzip static files to temporary directory
def unzip(source,dest_dir):
    with zipfile.ZipFile(source, "r") as z:
        z.extractall(dest_dir)

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


def download_file(src,dest):
    try:
        requester = urllib.URLopener()
        requester.retrieve(src, dest)
        return True
    except:
        print("Cannot download %s" %src)
        return False


# Filenames
def get_name(path):
    return os.path.split(path)[1].split(".")[0]

def get_random_name(length=6,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

# Generate new png paths to correspond to nifti filenames
def make_png_paths(nifti_files):
    image_paths = []
    for i in range(0,len(mr_files)):
        image = mr_files[i]
        tmp_svg = "%s/tmpbrain%s.png" %(tmp_dir,i)
        make_glassbrain_image(image,tmp_svg)
        image_paths.append(tmp_svg)
    return image_paths

def get_extension(path):
    fileparts =  os.path.basename(path).split(".")
    fileparts.pop(0)
    return ".".join(fileparts)

# Get unique values in a list of lists
def unwrap_list_unique(list_of_lists):
    uniques = []
    for listy in list_of_lists:
        uniques = uniques + [item for item in listy]
    uniques = list(np.unique(uniques))
    return uniques

# Brain image templates
def get_standard_brain(load=True):
    mr_directory = get_package_dir()
    brain = "%s/data/MNI152_T1_2mm_brain.nii.gz" %(mr_directory)
    if load:
        return nib.load(brain)
    else:
        return brain

# Check if nifti is empty
def is_empty(nii_file):
    nii = nibabel.load(nii_file)
    data = nii.get_data()
    data = numpy.nan_to_num(data)
    if numpy.count_nonzero(data) == 0:
        return 1
    return 0

def get_images(peaks,location_key):
    '''get_images returns unique images for a location key from
    a peaks table
    '''
    image_list = []
    for nidm,entries in peaks.items():
        nidm_directory = os.path.dirname(nidm)
        for e in range(len(entries)):
            if location_key in entries[e]:
                brainmap = entries[e][location_key]
                if brainmap not in image_list:
                    image_list.append(brainmap)
    return image_list
