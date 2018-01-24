#!/usr/bin/env python

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

from nidmviewer.viewer import generate
from glob import glob
import argparse
import sys
import os

def main():

    parser = argparse.ArgumentParser(
    description="command line or server tool to view or compare nidm results.")

    parser.add_argument("ttl", type=str,
                         help="List of comma separated ttl files to parse.")

    parser.add_argument("--base", type=str,
                         help="base image (standard brain map) to use for the viewer background.")

    parser.add_argument("--port", type=int,
                         help="PORT to use to serve nidmviewer (default 8088).")

    parser.add_argument("--columns_to_remove", type=str, 
                         default="statmap_filename,excsetmap_location,statmap_type",
                         help="Comma separated list of columns to remove from viewer.")
 
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    print("Starting up the nidmviewer!")

    nidm_files = args.ttl.split(",")
    if args.columns_to_remove != None:
        args.columns_to_remove = [x.strip(" ") for x in args.columns_to_remove.split(",")]
   
    nidm_files = [os.path.abspath(f) for f in nidm_files]
    if args.base is not None:
        standard_brain = os.path.abspath(args.base)
    else:
        standard_brain = None

    httpd = generate(ttl_files=nidm_files,
                     base_image=standard_brain,
                     columns_to_remove=args.columns_to_remove,
                     view_in_browser=True,
                     port=args.port)

if __name__ == '__main__':
    main()
