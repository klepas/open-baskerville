#!/usr/bin/python

"""Calls the compiler.
To reproduce the output in this folder:
$ ./ufo2otf.py OpenBaskerville.ufo OpenBaskerville-afdko.otf afdko
(requires ufo2fdk, robofab, afdko)
$ ./ufo2otf.py OpenBaskerville.ufo OpenBaskerville-fontforge.otf fontforge
(requires fontforge and scripting extensions)
"""

from sys import argv, exit

if len(argv) != 4:
    print """usage: ./ufo2otf.py infile.ufo outfile.otf compiler
    compiler: fontforge or afdko"""
    exit()
else:
    if argv[3] == 'fontforge':
        from compile import Fontforge as compiler
    elif argv[3] == 'afdko':
        from compile import Afdko as compiler
    else:
        print "unrecognised compiler %s" % argv[3]
        exit()

compile = compiler(argv[1],argv[2])
compile.compile()