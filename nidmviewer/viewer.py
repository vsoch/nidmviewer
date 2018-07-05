'''
viewer.py: part of the nidmviewer package

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
from nidmviewer.utils import strip_url, get_random_name, get_extension, \
 download_file, get_standard_brain, is_empty, get_images
from nidmviewer.templates import get_template, add_string, save_template, remove_resources
from nidmviewer.sparql import get_coordinates_and_maps
from nidmviewer.convert import parse_coordinates
from nidmviewer.browser import view
import pandas
import numpy
import os
import sys


def generate(ttl_files,base_image=None,retrieve=False,view_in_browser=False,columns_to_remove=None,
             template_choice="index",port=None,remove_scripts=None,button_text="BRAIN",check_empty=False):
    '''generate
    will generate a nidmviewer to run locally or to embed into webserver
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
    '''

    # Check inputs and prepare template        
    ttl_files = check_inputs(ttl_files)
    template = get_template(template_choice)  

    if remove_scripts != None:
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
    if columns_to_remove != None:
        if isinstance(columns_to_remove,str):
            columns_to_remove = [columns_to_remove]
        columns = columns_to_remove + columns
    column_names = remove_columns(column_names,columns)

    # We want pandas df in the format of dict/json strings for javascript embed
    for nidm,peak in peaks.items():
        peaks[nidm] = to_dictionary(peak,strings=True)    
 
    # Retrieve nifti files, if necessary
    peaks = retrieve_nifti(peaks,retrieve,"excsetmap_location")

    template = add_string("[SUB_FILELOCATIONKEY_SUB]","excsetmap_location",template)
    template = add_string("[SUB_FILENAMEKEY_SUB]","statmap",template)
    template = add_string("[SUB_COLUMNS_SUB]",str(column_names),template)
    template = add_string("[SUB_BUTTONTEXT_SUB]",button_text,template)

    # If excursion set is empty (regardless of peaks listed in the .ttl file) show "No suprathreshold voxels" instead of the table and the nifiti viewer. (this will happen if the analysis did not return any statistically significant results)
    empty_images = dict()

    if view_in_browser==True:
        peaks,copy_list = generate_temp(peaks,"excsetmap_location")

        for exc_set_file,image_name in copy_list.items():
            if check_empty == True:
                empty_images[image_name] = is_empty(exc_set_file)
            else:
                empty_images[image_name] = 0

        if base_image is None:
            base_image = get_standard_brain(load=False)
            dummy_peak = {base_image: [{"excsetmap_location":base_image}]}
            junk,base_copy = generate_temp(dummy_peak,"excsetmap_location")
            copy_list.update(base_copy)
            base_image = list(base_copy.values())[0]
        
        template = add_string("[SUB_EMPTY_SUB]",str(empty_images),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        view(template,copy_list,port)

    else:
        if base_image == None:
            base_image = get_standard_brain(load=False)

        image_files = get_images(peaks,"excsetmap_location")
        for image_file in image_files:
            if check_empty == True:
                empty_images[image_file] = is_empty(image_file)
            else:
                empty_images[image_file] = 0

        template = add_string("[SUB_EMPTY_SUB]",str(empty_images),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        return template


def parse_nidm(ttl_files):
    '''parse_nidm
        Extract brainmaps and coordinates from ttl files
    Parameters:
    ==========
    ttl_files: list
        list of full paths to ttl files
    Returns
    =======
    peaks: dict
        dict of pandas data frames, one for each ttl_file, with columns
        coordinate, z, peak_name, pvalue_uncorrected
    maps: dict
        dict of pandas data frames, one for each ttl_file, with columns
        filename and location for all brain maps specified in ttl.
    '''
    peaks = dict()
    for n in range(len(ttl_files)):
        ttl_file = os.path.abspath(ttl_files[n])
        df = get_coordinates_and_maps(ttl_file)
        peaks[ttl_file] = df
    return peaks


def to_dictionary(df,orient="records",strip_columns=False,strings=False):
    '''to_dictionary: 
       Convert a pandas dataframe into the string of a json/dict to 
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


def retrieve_nifti(peaks,retrieve,location_key):
    '''retrieve_nifti
    Download the image to a temporary folder if the user needs to
    retrieve it. Otherwise, return file
    Parameters
    ==========
    peaks: dict
        dictionary (key, is ttl_file, and value, is dictionary of {filename:fullpath}
        for all brainmaps extracted from the ttl files
    retrieve: boolean
        if True, will download brainmaps to temporary folder first. If false, encodes
        path in utf-8 for rendering in javascript
    location_key: str
        key to look up file name in peaks dictionary
    '''
    # Note: retrieve = True has not been tested!
    updated_peaks = dict()
    for nidm,entries in peaks.items():
        if retrieve:
            for e in range(len(entries)):
                if location_key in entries[e]:
                    brainmap = entries[e][location_key]
                    image_ext = get_extension(brainmap)
                    temp_path = get_random_name()
                    temp_dir = tempfile.mkdtemp()
                    temp_image_path = "%s/%s.%s" %(temp_dir,temp_path,image_ext)
                    if download_file(brainmap,temp_image_path):
                        entries[e][location_key] = temp_image_path
        updated_peaks[nidm] = entries
    return updated_peaks


def get_column_names(peaks):
    column_names = dict()
    for nidm,df in peaks.items():
        column_names[nidm] = df.columns.tolist()
    return column_names


def generate_temp(peaks,location_key):
    '''generate_temp
    generate a lookup of temporary files
    Parameters
    ==========
    peaks: dict
       data structure from get_coordinates_and_peaks
    location_key: str
       key in peaks data structure for file paths
    Returns
    =======
    peaks: dict
        (key is ttl file, equivalent to peaks, but old location_key path is replaced
        with path to temporary directory
    copy_list: dict
        keys are current paths, values are temporary file names corresponding to
        fullpath in new_nifti_files[ttl_file] dictionary. This is used to copy
        images into the temporary directory with the correct names. 
    '''
    copy_list = dict()
    for nidm,entries in peaks.items():
        nidm_directory = os.path.dirname(nidm)
        for e in range(len(entries)):
            if location_key in entries[e]:
                brainmap = entries[e][location_key]
                brainmap_base = os.path.basename(brainmap)
                if "%s/%s" %(nidm_directory,brainmap_base) not in copy_list:
                    image_ext = get_extension(brainmap)
                    temp_path = get_random_name()
                    temp_image_path = "%s.%s" %(temp_path,image_ext)
                    copy_list["%s/%s" %(nidm_directory,brainmap_base)] = temp_image_path

    updated_peaks = dict()

    for nidm,entries in peaks.items():
        nidm_directory = os.path.dirname(nidm)
        to_keep = []
        for e in range(len(entries)):
            if location_key in entries[e]:
                brainmap = entries[e][location_key]
                brainmap_base = os.path.basename(brainmap)
                entries[e][location_key] = copy_list["%s/%s" %(nidm_directory,brainmap_base)]
                if "x" in entries[e]:
                    if entries[e]["x"] != "nan":
                        to_keep.append(e)

        # Remove coordinates that are nan from the data frame
        entries = [entries[e] for e in range(len(entries)) if e in to_keep]
        updated_peaks[nidm] = entries

    return updated_peaks,copy_list 


def check_inputs(ttl_files):
    """check_input.
    will return a list of ttl files, more advanced
    functionality can be added if needed (validation, etc)
    Parameters
    ==========
    ttl_files: string or list
        full paths to ttl files   
    Returns
    =======
        list of ttl files
    """
    if isinstance(ttl_files,str): ttl_files = [ttl_files]
    return ttl_files

def remove_columns(columns,columns_to_remove):
    new_columns = dict()
    for nidm,column_names in columns.items():
        new_columns[nidm] = [x for x in column_names if x not in columns_to_remove]        
    return new_columns
