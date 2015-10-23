'''
viewer.py: part of the nidmviewer package

'''
from nidmviewer.utils import strip_url, get_random_name, get_extension, download_file, get_standard_brain
from nidmviewer.templates import get_template, add_string, save_template
from nidmviewer.sparql import get_coordinates, get_brainmaps
from nidmviewer.convert import getjson
from nidmviewer.browser import view
import os
import sys


def generate(ttl_files,base_image=None,retrieve=False,view_in_browser=False,
             columns_to_remove=None,template_choice="index",port=None):
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
    port: int
        port to serve nidmviewer, if view_in_browser==True
    '''

    # Check inputs and prepare template        
    ttl_files = check_inputs(ttl_files)
    template = get_template(template_choice)  

    # Parse each nidm file
    peaks,brainmaps = parse_nidm(ttl_files)

    # if the user wants to remove columns
    if columns_to_remove != None:
        peaks = remove_columns(peaks,columns_to_remove)

    # Grab the column names, it could be different for each ttl
    column_names = get_column_names(peaks)

    # We want pandas df in the format of dict/json strings for javascript embed
    for nidm,peak in peaks.iteritems():
        peaks[nidm] = to_dictionary(peak,strings=True)    
    for nidm,maps in brainmaps.iteritems():
        brainmaps[nidm] = to_dictionary(maps,strip_columns=True)[0]    

    # Retrieve nifti files, if necessary
    nifti_files = retrieve_nifti(brainmaps,retrieve)

    if view_in_browser==True:
        tmp_nifti_files,copy_list = generate_temp(nifti_files)
        if base_image == None:
            base_image = get_standard_brain(load=False)
            tmp_base_image,base_copy = generate_temp({base_image: {base_image:base_image}})
            copy_list.update(base_copy)
            base_image = base_copy.values()[0]
        template = add_string("[SUB_BRAINMAPS_SUB]",str(tmp_nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        template = add_string("[SUB_COLUMNS_SUB]",str(column_names),template)
        view(template,copy_list,port)

    else:
        # We will embed json/objects in the page to render dynamically
        template = add_string("[SUB_BRAINMAPS_SUB]",str(nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        template = add_string("[SUB_COLUMNS_SUB]",str(column_names),template)
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
    maps = dict()
    for n in range(len(ttl_files)):
        ttl_file = os.path.abspath(ttl_files[n])
        df = get_coordinates(ttl_file)
        brainmaps = get_brainmaps(ttl_file)
        peaks[ttl_file] = df
        maps[ttl_file] = brainmaps
    return peaks,maps


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

def retrieve_nifti(maps,retrieve):
    '''retrieve_nifti
    Download the image to a temporary folder if the user needs to
    retrieve it. Otherwise, return file
    Parameters
    ==========
    maps: dict
        dictionary (key, is ttl_file, and value, is dictionary of {filename:fullpath}
        for all brainmaps extracted from the ttl files
    retrieve: boolean
    if True, will download brainmaps to temporary folder first. If false, encodes
    path in utf-8 for rendering in javascript
    '''
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
    '''generate_temp
    generate a lookup of temporary files
    Parameters
    ==========
    nifti_files: dictionary 
        (key is ttl file, value is dictionary of nifti files {filename:fullpath}
    Returns
    =======
    new_nifti_files: dict
        (key is ttl file, value is dictionary of nifti files {filename:fullpath}
        equivalent files but without path as all files will go in same level
        of the temporary directory
    copy_list: dict
        keys are current paths, values are temporary file names corresponding to
        fullpath in new_nifti_files[ttl_file] dictionary. This is used to copy
        images into the temporary directory with the correct names. 
    '''
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

def remove_columns(peaks,columns_to_remove):
    newpeaks = dict()
    for nidm,df in peaks.iteritems():
        for column_name in columns_to_remove:
            if column_name in df:
                df = df.drop(column_name,axis=1)
        newpeaks[nidm] = df
    return newpeaks
