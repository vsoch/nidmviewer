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

from nidmviewer.utils import make_tmp_folder
from nidmviewer.templates import get_favicon
import webbrowser
import shutil
import os

try:
    import SimpleHTTPServer
    import SocketServer
except:
    import http.server as SimpleHTTPServer
    import socketserver as SocketServer

def view(html_snippet, peaks, port, location_key):
    '''view code in temporary browser. This function moves the files so
       they are served from a common (temporary) root.

       Parameters
       ==========
       html_snippet is the template code with images subbed
       peaks is a dictionary, with {nidm: []}} where each nidm has a list
             of dict entries with excsetmap_locations and an original_path
             to copy to a temporary folder
    '''
    with make_tmp_folder() as tmp_dir:  

        # Put a favicon there
        favicon = get_favicon()
        shutil.copy(favicon, tmp_dir)

        # First copy all brain maps that aren't served via http
        for nidm, images in peaks.items():
            for item in images:
                
                # Viewer is flexible to find local path or url
                image_path = item[location_key]

                # If we have a local file, not web address
                if os.path.exists(image_path):
                    tmp_name = os.path.basename(image_path)
                    final_path = "%s/%s" %(tmp_dir, tmp_name)

                    # And it must exist in the web root
                    if not os.path.exists(final_path):
                        shutil.copy(image_path, final_path)
                    
        # Now write template to temporary file
        tmp_file = "%s/pycompare.html" %(tmp_dir)

        # Change directory and start a web server
        os.chdir(tmp_dir)
        print(os.getcwd())
        write_file(html_snippet, tmp_file)

        tmp_file_base = os.path.basename(tmp_file)

        if port is not None:
            httpd = run_webserver(html_page="%s" %(tmp_file_base), port=port)
        else:
            httpd = run_webserver(html_page="%s" %(tmp_file_base))
        return httpd


def write_file(html_snippet, tmp_file):
    '''write a html_snippet content to a file (tmp_file)
    '''
    with open(tmp_file,'w') as html_file:
        if isinstance(html_snippet, bytes):
            html_snippet = html_snippet.decode('utf-8')
        html_file.writelines(html_snippet)
    return tmp_file


def run_webserver(port=None, html_page="index.html"):
    '''Web server (for Papaya Viewer in QA report
    '''

    if port is None:
        port = 8088

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    print("Serving nidmviewer at port %s" %port)
    webbrowser.open("http://localhost:%s/%s" %(port,html_page))
    httpd.serve_forever()
    return httpd

def get_svg_html(mpl_figures):
    '''Get svg html from matplotlib figures (eg, glass brain images)
    '''

    svg_images = []
    with make_tmp_folder() as tmp_dir:  
        for fig in mpl_figures:
            tmp_svg = "%s/mplfig.svg" %(tmp_dir)
            fig.savefig(tmp_svg)
            fig_data = open(tmp_svg,"rb").readlines()
            svg_images.append(fig_data)
    return svg_images
