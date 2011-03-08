#!/usr/bin/python

from diagnostics import diagnostics, known_compilers, FontError

diagnostics = diagnostics()

class Compiler:
    def __init__(self,infile,outfile,compiler=None):
        self.infile = infile
        self.outfile = outfile
        if compiler:
            if compiler in known_compilers and diagnostics[compiler]:
                self.compile = getattr(self, compiler)
            else:
                raise FontError(compiler, diagnostics)
        else:
            if diagnostics['fontforge']:
                self.compile = self.fontforge
            elif diagnostics['afdko']:
                self.compile = self.afdko
            else:
                raise FontError(diagnostics=diagnostics)

    def fontforge(self):
        import fontforge
        font = fontforge.open(self.infile)
        font.generate(self.outfile,flags=("round"))
        
    def afdko(self):
        import ufo2fdk
        from robofab.objects.objectsRF import RFont
        compiler = ufo2fdk.OTFCompiler()
        font = RFont(self.infile)
        compiler.compile(font,self.outfile,releaseMode=True)

