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

def get_favicon():
    ppwd = get_package_dir()
    return os.path.abspath(os.path.join(ppwd,'template', 'favicon.ico'))    

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
