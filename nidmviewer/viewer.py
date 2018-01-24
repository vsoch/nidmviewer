'''

Copyright (c) 2014-2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''


from nidmviewer.utils import (
    download_file,
    get_redirect_url,
    get_standard_brain, 
    is_empty
)

from nidmviewer.templates import (
    add_string,
    get_template,
    remove_resources,
    save_template,
)

from nidmviewer.sparql import get_coordinates_and_maps
from nidmviewer.convert import parse_coordinates
from nidmviewer.browser import view

import pandas
import tempfile
import os
import re
import sys


def generate(ttl_files,
             base_image=None,
             retrieve=False,
             view_in_browser=False,
             columns_to_remove=None,
             template_choice="index",
             port=None,
             remove_scripts=None,
             button_text="BRAIN",
             check_empty=False,
             location_key="excsetmap_location",
             relative_to=''):

    ''' generate a nidmviewer to run locally or to embed into webserver

    Parameters
    ==========

    ttl_files: str or list 
        one or more turtle files to add to the viewer. Images in the files should be available
        at the specified URL. 
    retrieve: boolean
        If set to False, the images are assumed to be on the same server, and will be 
        served with the given URL. If retrieve is set to True, the images will be retrieved
        first and stored in a temporary directory.
    base_image: str
        The base image to use for the viewer. Not specifying a base_image will
        yield a black background.
    view_in_browser: boolean
        open a temporary web browser (to run locally). If True, images will be copied
        to a temp folder. If False, image_paths must be relative to web server. File names 
        should be unique.
    columns_to_remove: additional columns to remove. If none, default columns of "coordinate_id"
        "statmap_type" and "exc_set" will be removed.
    port: int
        port to serve nidmviewer, if view_in_browser==True
    remove_scripts: list
        one or more script or button tags to remove from the template. Options include
        JQUERY BOOTSTRAPJS BOOTSTRAPCSS PAPAYACSS PAPAYAJS NIDMSELECTBUTTON
    button_text: str
        Text string for the button to select a brain image. Default is "BRAIN"
    check_empty: boolean - check for empty images or not. Will result in error if nidm paths
               are URLS.
    location_key: the path/url to the file in the nidm result, defaults to "excsetmap_location"
    relative_root: if view is set to False and an html_snippet is returned, serve the images relative to 
              this web_root path.

    '''

    # Check inputs and prepare template        
    ttl_files = check_inputs(ttl_files)
    template = get_template(template_choice)  

    if remove_scripts is not None:
        if isinstance(remove_scripts,str):
            remove_scripts = [remove_scripts]
        template = template.split("\n")
        resources = ["TAG_%s_TAG" %x for x in remove_scripts]
        template = remove_resources(template,resources)
        template = "\n".join(template)

    # Parse each nidm file
    peaks = parse_nidm(ttl_files)

    # Convert coordinates from '[x,y,z]' to [x],[y],[z]
    for nidm,peak in peaks.items():
        coordinates = parse_coordinates(peak.coordinate.tolist())
        peak = peak.drop("coordinate",axis=1)
        if coordinates.shape[0] > 0:
            peak["x"] = coordinates["x"].tolist()
            peak["y"] = coordinates["y"].tolist()
            peak["z"] = coordinates["z"].tolist()
        peaks[nidm] = peak

    # Grab the column names, it could be different for each ttl
    column_names = get_column_names(peaks)

    # if the user wants to remove columns
    columns = ["coordinate_id","exc_set","statmap_type"]
    if columns_to_remove is not None:
        if isinstance(columns_to_remove,str):
            columns_to_remove = [columns_to_remove]
        columns = columns_to_remove + columns
    column_names = remove_columns(column_names,columns)

    # We want pandas df in the format of dict/json strings for javascript embed
    for nidm,peak in peaks.items():
        peaks[nidm] = to_dictionary(peak,strings=True)
 
    # Retrieve nifti files, if necessary
    peaks = retrieve_nifti(peaks, retrieve, location_key)

    template = add_string("[SUB_FILELOCATIONKEY_SUB]", location_key, template)
    template = add_string("[SUB_FILENAMEKEY_SUB]", "statmap", template)
    template = add_string("[SUB_COLUMNS_SUB]", str(column_names), template)
    template = add_string("[SUB_BUTTONTEXT_SUB]", button_text, template)

    # If excursion set is empty (regardless of peaks listed in the .ttl file) 
    # show "No suprathreshold voxels" instead of the table and nifiti viewer
    # (this will happen if the analysis did not return any 
    # statistically significant results)

    if base_image is None:
        base_image = get_standard_brain()

    # Update the data structure to include paths to copy the images
    peaks = clean_peaks(peaks, location_key, relative_to)

    # Get a lookup for empty (1) or non empty maps (1)
    # assumes file path is at 'original_file' index in peaks set in clean_peaks
    empty_images = is_empty(peaks, check_empty, location_key) 

    template = add_string("[SUB_EMPTY_SUB]", str(empty_images),template)
    template = add_string("[SUB_PEAKS_SUB]", str(peaks),template)
    template = add_string("[SUB_BASEIMAGE_SUB]", str(base_image),template)

    # Add the base image
    peaks[base_image] = [{location_key: base_image}]

    if view_in_browser is True:
        view(template, peaks, port, location_key)

    return template


def parse_nidm(ttl_files):
    '''Extract brainmaps and coordinates from ttl files

       Parameters:
       ==========
       ttl_files: list
           list of full paths to ttl files

       Returns
       =======
       peaks: dict of pandas data frames, one for each ttl_file, with columns
              coordinate, z, peak_name, pvalue_uncorrected
       maps:  dict of pandas data frames, one for each ttl_file, with columns
              filename and location for all brain maps specified in ttl.
    
    '''
    peaks = dict()
    for n in range(len(ttl_files)):
        ttl_file = os.path.abspath(ttl_files[n])
        df = get_coordinates_and_maps(ttl_file)
        peaks[ttl_file] = df
    return peaks


def to_dictionary(df,orient="records",strip_columns=False,strings=False):
    '''Convert a pandas dataframe into the string of a json/dict to 
       embed into page
       
       Parameters
       ==========
       df: pandas data frame
           data frame to convert
       orient: str
           orientation to convert with (default is "records")
       strip_columns: boolean
           if true, will return df.to_dict(orient=orient).values()
           default is False
       strings: boolean
           True will convert all columns to strings.
    '''
    if strings:
        for column in df.columns:
            df[column] = df[column].astype(str)
    if strip_columns:
        return df.to_dict().values() 
    else:
        return df.to_dict(orient=orient)


def retrieve_nifti(peaks, retrieve, location_key, download_folder=None):
    '''Download the image to a temporary folder if the user needs to
       retrieve it. Otherwise, return file
    
       Parameters
       ==========
        peaks: dictionary (key, is ttl_file, and value, is dictionary of 
               {filename:fullpath} for all brainmaps extracted from ttl files
        retrieve: if True, will download brainmaps to temporary folder first.
                  if False, encodes path in utf-8 for rendering in javascript
        location_key: key to look up file name in peaks dictionary

    '''
    updated_peaks = dict()

    # Keep track of those we have downloaded
    seen = dict()

    # Ensure images downloaded to same folder, only if retrieved
    if download_folder is None and retrieve is True:
        download_folder = tempfile.mkdtemp()

    for nidm,entries in peaks.items():
        for e in range(len(entries)):
            if location_key in entries[e]:

                # This can be a url or a file
                brainmap = entries[e][location_key]

                # We haven't seen it yet
                if brainmap in seen:
                    entries[e][location_key] = seen[brainmap]
                else:

                    # Return successful download OR original path
                    if retrieve is True:
                        download_path = download_file(src=brainmap, 
                                                      download_folder=download_folder)                 
                    # Just return the path
                    else:
                        download_path = brainmap

                    entries[e][location_key] = download_path
                    seen[brainmap] = download_path

        # Update the peaks lookup with entries list
        updated_peaks[nidm] = entries
    return updated_peaks


def get_column_names(peaks):
    column_names = dict()
    for nidm,df in peaks.items():
        column_names[nidm] = df.columns.tolist()
    return column_names


def clean_peaks(peaks, location_key, relative_to=''):
    '''update peaks data structure to include a location_key that has redirects
       followed, and optionally is relative to a local (user specified) path.
       remove entries with nan values.
    
       Parameters
       ==========
       peaks: (dict) data structure from get_coordinates_and_peaks
       location_key: (str) key in peaks data structure for file paths
       relative: (bool) if True, user wants to generate relative to $PWD and
                        nidm file (e.g., fsl/nidm.ttm --> fsl/brainmap.nii.gz)

       Returns
       =======
       updated_peaks: the same peaks data structure with nan peaks removed
    '''

    # prepare to copy files we have locally
    updated_peaks = dict()
    lookup = dict()         # don't follow redirect more than once per map

    for nidm, entries in peaks.items():

        # index to coordinates to keep
        to_keep = []

        for e in range(len(entries)):

            if location_key in entries[e]:

                brainmap = entries[e][location_key]

                # Generate a name for the brainmap, unless one provided
                if not brainmap.startswith('http'):
                    name = "%s%s" %(relative_to, os.path.basename(brainmap))
                else:
                    name = brainmap

                # The location_key cooresponds with the file to be served
                if name not in lookup:
                    lookup[name] = get_redirect_url(name)
                entries[e][location_key] = lookup[name]

                if "x" in entries[e]:
                    if entries[e]["x"] != "nan":
                        to_keep.append(e)
                        
                entries[e]['original_path'] = brainmap

        # Remove coordinates that are nan from the data frame
        entries = [entries[e] for e in range(len(entries)) if e in to_keep]
        updated_peaks[nidm] = entries

    return updated_peaks


def check_inputs(ttl_files):
    '''check_input.
        will return a list of ttl files, more advanced
        functionality can be added if needed (validation, etc)
    
        Parameters
        ==========
        ttl_files: string or list. full paths to ttl files   

        Returns
        =======
        list of ttl files
    '''
    if isinstance(ttl_files,str): ttl_files = [ttl_files]
    return ttl_files


def remove_columns(columns,columns_to_remove):
    '''remove one or more columns from the data frame to be rendered in
       the web interface
    '''

    new_columns = dict()
    for nidm,column_names in columns.items():
        new_columns[nidm] = [x for x in column_names if x not in columns_to_remove]        
    return new_columns
