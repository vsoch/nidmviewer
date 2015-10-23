'''
templates.py: part of the nidmviewer package
Functions to work with html templates

'''

from nidmviewer.utils import get_package_dir
import pandas
import os
import re

def get_template(html_name):
    return read_template(html_name)

# Add code string to end of template
def add_javascript_function(function_code,template):
    template.append("<script>\n%s\n</script>" % (function_code))
    return template

# Remove scripts (css or js) from html_snippet
def remove_resources(html_snippet,script_names):
    expression = re.compile("|".join(script_names))
    filtered_template = [x for x in html_snippet if not expression.search(x)]
    return filtered_template

def save_template(html_snippet,output_file):
    filey = open(output_file,"wb")
    filey.writelines(html_snippet)
    filey.close()

def read_template(html_name):
    ppwd = get_package_dir()  
    html_name = html_name + ".html"
    template_file = os.path.abspath(os.path.join(ppwd,'template', html_name))
    filey = open(template_file,"r")
    template = "".join(filey.readlines())
    filey.close()
    return template

def add_string(tag,substitution,template):
    template = template.replace(tag,substitution)
    return template

'''Get an image by name in the img directory'''
def get_image(image_name):
    ppwd = get_package_dir()  
    return os.path.join(ppwd,'img', image_name)
