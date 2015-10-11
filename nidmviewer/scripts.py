#!/usr/bin/env python

'''
script.py: part of nidmviewer package
Functions to visualize in browser

'''

from nidmviewer.viewer import generate
from glob import glob
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
    description="command line or server tool to view or compare nidm results.")
    parser.add_argument("ttl", help="List of comma separated ttl files to parse.", type=str)
    parser.add_argument("base", help="base image (standard brain map) to use for the viewer background.",type=str)
    parser.add_argument("--columns_to_remove", help="Comma separated list of columns to remove from viewer.",type=str,default=None)
 
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    print "Starting up the nidmviewer!"

    nidm_files = args.ttl.split(",")
    if args.columns_to_remove != None:
        args.columns_to_remove = [x.strip(" ") for x in args.columns_to_remove.split(",")]
   
    nidm_files = [os.path.abspath(f) for f in nidm_files]
    standard_brain = os.path.abspath(args.base)
    httpd = generate(ttl_files=nidm_files,
                   base_image=standard_brain,
                   columns_to_remove=args.columns_to_remove,
                   view_in_browser=True)

if __name__ == '__main__':
    main()
