'''
browser.py: part of nidmviewer package
Functions to visualize in browser

'''
from nidmviewer.utils import make_tmp_folder
import webbrowser
import shutil
import os

try:
    import SimpleHTTPServer
    import SocketServer
except:
    import http.server as SimpleHTTPServer
    import socketserver as SocketServer

'''
View code in temporary browser!
html_snippet is the template code with images subbed
copy_list is a dictionary, 
  with {nidm:{brainmap1_file:temp1_file,..brainmapN_file:tempN_file}}
'''
def view(html_snippet, copy_list, port):

    with make_tmp_folder() as tmp_dir:  

        # First copy all brain maps
        for original, images in copy_list.items():
            for image in images:
                final_path = "%s/%s" %(tmp_dir, os.path.basename(image))
                if not os.path.exists(final_path):
                    shutil.copy(image, final_path)

        # Now write template to temporary file
        tmp_file = "%s/pycompare.html" %(tmp_dir)

        # Change directory and start a web server
        os.chdir(tmp_dir)
        print(os.getcwd())
        write_file(html_snippet, tmp_file)

        tmp_file_base = os.path.basename(tmp_file)
        if port!=None:
            httpd = run_webserver(html_page="%s" %(tmp_file_base),port=port)
        else:
            httpd = run_webserver(html_page="%s" %(tmp_file_base))
        return httpd


'''Internal view function'''
def internal_view(html_snippet,tmp_file):
    url = 'file://%s' %(tmp_file)
    write_file(html_snippet, tmp_file)
    webbrowser.open_new_tab(url)
    raw_input("Press Enter to finish...")

def write_file(html_snippet, tmp_file):
    html_file = open(tmp_file,'w')
    if isinstance(html_snippet, bytes):
        html_snippet = html_snippet.decode('utf-8')
    html_file.writelines(html_snippet)
    html_file.close()

'''Web server (for Papaya Viewer in QA report'''
def run_webserver(port=8088,html_page="index.html"):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    print("Serving nidmviewer at port %s" %port)
    webbrowser.open("http://localhost:%s/%s" %(port,html_page))
    httpd.serve_forever()
    return httpd

"""Get svg html from matplotlib figures (eg, glass brain images)"""
def get_svg_html(mpl_figures):
    svg_images = []
    with make_tmp_folder() as tmp_dir:  
        for fig in mpl_figures:
            tmp_svg = "%s/mplfig.svg" %(tmp_dir)
            fig.savefig(tmp_svg)
            fig_data = open(tmp_svg,"rb").readlines()
            svg_images.append(fig_data)
    return svg_images
