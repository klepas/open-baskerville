#!/usr/bin/python
# -*- coding: utf-8 -*-
# Todo: use argparse. add option to print diagnostics. 
# Make ufo2otf a python package, provide this script as a command line utility
# (I couldn’t figure out how, in distutils, one can specify for scripts to be
# installed into bin?)

"""Calls the compiler.
"""
from ufo2otf import Compiler

def console():
    import argparse
    from sys import exit

    parser = argparse.ArgumentParser()
    parser.add_argument("infiles", help="The source UFO files", nargs='+')
    
    parser.add_argument("--webfonts", help="Generate webfonts in a ./webfonts subfolder",
                    action="store_true")
    parser.add_argument("--afdko", help="Generate the OTF with Adobe Font Development Kit for Opentype",
                    action="store_true")
    args = parser.parse_args()
    
    if args.webfonts and args.afdko:
        exit("Can not generate webfonts through the AFDKO, exiting.")

    c = Compiler(args.infiles, args.webfonts, args.afdko)
    c.compile()

if __name__ == "__main__":
    console()
