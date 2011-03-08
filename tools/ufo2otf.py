#!/usr/bin/python
# -*- coding: utf-8 -*-
# Todo: use argparse. add option to print diagnostics. 
# Make ufo2otf a python package, provide this script as a command line utility
# (I couldn’t figure out how, in distutils, one can specify for scripts to be
# installed into bin?)

"""Calls the compiler.
"""

from sys import argv, exit
import ufo2otf

if 3 <= len(argv) <= 4:
    args = argv[1:]
    compiler = ufo2otf.Compiler(*args)
    compiler.compile()
else:
    print """usage: ./ufo2otf.py infile.ufo outfile.otf [compiler]
compiler: fontforge or afdko"""