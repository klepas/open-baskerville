#!/usr/bin/python

""" Defines possible font compile interfaces
    ( Call with ufo2otf.py )"""

class Fontforge:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
    
    def compile(self):
        import fontforge
        font = fontforge.open(self.infile)
        font.generate(self.outfile,flags=("round"))

class Afdko:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
    
    def compile(self):
        import ufo2fdk
        from robofab.objects.objectsRF import RFont
        compiler = ufo2fdk.OTFCompiler()
        font = RFont(self.infile)
        compiler.compile(font,self.outfile,releaseMode=True)
