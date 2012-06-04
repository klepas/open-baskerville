#!/usr/bin/python

from os import mkdir
from os.path import splitext, dirname, sep, join, exists, basename
from codecs import open
from diagnostics import diagnostics, known_compilers, FontError

diagnostics = diagnostics()

class Compiler:
    def __init__(self,infiles,webfonts=False,afdko=False):
        # we strip trailing slashes from ufo names,
        # otherwise we get confused later on when
        # generating filenames:
        self.infiles = [i.strip(sep) for i in infiles]
        self.webfonts = webfonts
        self.css = ''

        if afdko:
            if diagnostics['afdko']:
                self.compile = self.afdko
            else:
                raise FontError("afdko", diagnostics)
        else:
            if diagnostics['fontforge']:
                self.compile = self.fontforge
            else:
                raise FontError("fontforge", diagnostics)

    def fontforge(self):
        import fontforge
        for infile in self.infiles:
            outdir = dirname(infile)
            name = splitext(infile)[0]
            font = fontforge.open(infile)
            font.generate(name + '.otf', flags=("round"))
            
            if self.webfonts:
                webfonts_path = join(outdir, 'webfonts')
                print webfonts_path
                if not exists(webfonts_path):
                    mkdir(webfonts_path)

                font.autoHint()
                font.generate(join(outdir, 'webfonts', basename(name) + '.ttf'), flags=("round"))
                font.generate(join(outdir, 'webfonts', basename(name) + '.woff'), flags=("round"))
        
        if self.css:
            c = open(join(dirname(infiles[0]), 'webfonts','style.css'),'w','UTF-8')
            c.write(self.css)
            c.close()

    def afdko(self):
        import ufo2fdk
        from robofab.objects.objectsRF import RFont
        compiler = ufo2fdk.OTFCompiler()
        for infile in self.infiles:
            outfile = splitext(infile)[0] + '.otf'
            font = RFont(infile)
            compiler.compile(font, outfile, releaseMode=True)

