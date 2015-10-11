'''
viewer.py: part of the nidmviewer package

'''
import os
import sys
from nidmviewer.convert import getjson
from nidmviewer.query import get_peaks_and_maps
from nidmviewer.utils import strip_url, get_random_name, get_extension, download_file
from nidmviewer.templates import get_template, add_string, save_template
from nidmviewer.browser import view


"""
generate

will generate a nidmviewer to run locally [not yet developed] or to embed into webserver

ttl_files: one or more turtle files to add to the viewer. Images in the files should be available
      at the specified URL. 
provn_files: NOT YET IMPLEMENTED.
retrieve: If set to False, the images are assumed to be on the same server, and will be 
          served with the given URL. If retrieve is set to True, the images will be retrieved
          first and stored in a temporary directory.
base_image: The base image to use for the viewer. Not specifying a base_image will
            yield a black background.
view_in_browser: open a temporary web browser (to run locally). If True, images will be copied
      to a temp folder. If False, image_paths must be relative to web server. File names 
      should be unique.

"""
def generate(ttl_files,provn_files=None,base_image="",retrieve=False,view_in_browser=False,
             columns_to_remove=None,template_choice="index"):

    # Check inputs and prepare template        
    ttl_files,provn_files = check_inputs(ttl_files,provn_files)
    template = get_template(template_choice)  

    # Parse each nidm file, get nifti paths
    peaks,maps = parse_nidm(ttl_files,provn_files)
    nifti_files = retrieve_nifti(maps,retrieve)

    # if the user wants to remove columns
    if columns_to_remove != None:
        peaks = remove_columns(peaks,columns_to_remove)

    # Grab the column names, it could be different for each ttl
    column_names = get_column_names(peaks)

    # We want pandas df in the format of dict/json strings for javascript embed
    for nidm,peak in peaks.iteritems():
        peaks[nidm] = to_dictionary(peak)    

    # Nans need to be strings as well
    peaks_html = str(peaks)
    peaks_html = peaks_html.replace("nan","'nan'")

    if view_in_browser==True:
        tmp_nifti_files,copy_list = generate_temp(nifti_files)
        if base_image != "":
            tmp_base_image,base_copy = generate_temp({base_image: {base_image:base_image}})
            copy_list.update(base_copy)
            base_image = base_copy.values()[0]
        template = add_string("[SUB_BRAINMAPS_SUB]",str(tmp_nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",peaks_html,template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        template = add_string("[SUB_COLUMNS_SUB]",str(column_names),template)
        view(template,copy_list)

    else:
        # We will embed json/objects in the page to render dynamically
        template = add_string("[SUB_BRAINMAPS_SUB]",str(nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",peaks_html,template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        template = add_string("[SUB_COLUMNS_SUB]",str(column_names),template)
        return template


"""
Here we will parse the nidm files (RDF) into a far superior format (json)
It's not pretty, but it's simple to parse a json structure!

"""
def parse_nidm(ttl_files,provn_files):
    peaks = dict()
    maps = dict()
    for n in range(len(ttl_files)):
        ttl_file = os.path.abspath(ttl_files[n])
        if provn_files:
            provn_file = os.path.abspath(provn_files[n])
        ttl = getjson(ttl_file)
        df,brainmaps = get_peaks_and_maps(ttl)
        peaks[ttl_file] = df
        maps[ttl_file] = brainmaps
    return peaks,maps

"""
Convert a pandas dataframe into the string of a json/dict to 
embed into page

"""
def to_dictionary(df):
    return df.to_dict(orient="records")

"""
Download the image to a temporary folder if the user needs to
retrieve it. Otherwise, return file

"""
def retrieve_nifti(maps,retrieve):
    # Note: retrieve = True has not been tested!
    map_paths = dict()
    for nidm,maplist in maps.iteritems():
        if retrieve:
            single_maps = dict()
            for brainmap_id,brainmap in maplist.iteritems():
                image_ext = get_extension(brainmap)
                temp_path = get_random_name()
                temp_image_path = "%s.%s" %(temp_path,image_ext)
                if download_file(brainmap,temp_image_path):
                    single_maps[strip_url(brainmap_id)] = temp_image_path
        else:
            single_maps = dict()
            for brainmap_id,brainmap in maplist.iteritems():
                single_maps[strip_url(brainmap_id)] = brainmap.encode("utf-8") 
        map_paths[nidm] = single_maps
    return map_paths


def get_column_names(peaks):
    column_names = dict()
    for nidm,df in peaks.iteritems():
        column_names[nidm] = df.columns.tolist()
    return column_names

def generate_temp(nifti_files):
    # Here we will generate a lookup of temporary files
    new_nifti_files = dict()
    copy_list = dict()
    for nidm_file,maplist in nifti_files.iteritems():
        nidm_directory = os.path.dirname(nidm_file)
        single_maps = dict()
        for brainmap_id,brainmap in maplist.iteritems():
            brainmap_base = os.path.basename(brainmap)
            image_ext = get_extension(brainmap)
            temp_path = get_random_name()
            temp_image_path = "%s.%s" %(temp_path,image_ext)
            single_maps[strip_url(brainmap_id)] = temp_image_path
            copy_list["%s/%s" %(nidm_directory,brainmap_base)] = temp_image_path
        new_nifti_files[nidm_file] = single_maps
    return new_nifti_files,copy_list      


# Now sure if we will need this
def get_bootstrap():
    return ['<script src="https://rawgit.com/vsoch/nidmviewer/master/js/jquery-2.1.4.min.js"></script>','<link rel="stylesheet" type="text/css" href="https://rawgit.com/vsoch/nidmviewer/master/css/bootstrap.min.css">','<script src="https://rawgit.com/vsoch/nidmviewer/master/js/bootstrap.min.js"></script>']

def check_inputs(ttl_files,provn_files):
    if isinstance(ttl_files,str): ttl_files = [ttl_files]
    if provn_files:
        if isinstance(provn_files,str): provn_files = [provn_files]    
        if len(provn_files) == 1:
            provn_files = provn_files * len(ttl_files)
        elif len(provn_files) != len(ttl_files):
            print "You must specify 1 or %s provn files." %(len(ttl_files))
            sys.exit(32)
    return ttl_files,provn_files

def remove_columns(peaks,columns_to_remove):
    newpeaks = dict()
    for nidm,df in peaks.iteritems():
        for column_name in columns_to_remove:
            if column_name in df:
                df = df.drop(column_name,axis=1)
        newpeaks[nidm] = df
    return newpeaks
