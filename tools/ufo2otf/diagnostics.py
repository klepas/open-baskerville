#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import textwrap

known_compilers = ['fontforge','afdko']

def diagnostics():
    """
    Returns a dict with information about the state of possible build tools on
    the users system. This is probably better implemented as a class.
    """
    diagnostics = {}
    
    # FontForge
    # Via the Python bindings?
    try:
        import fontforge
        diagnostics['pyff'] = diagnostics['fontforge'] = True
    except ImportError:
        diagnostics['pyff'] = diagnostics['fontforge'] = False
    # The main fontforge program (with or without bindings):
    diagnostics['ff'] = subprocess.Popen(['which','fontforge'], stdout=subprocess.PIPE).communicate()[0].strip()    
    
    # The Adobe Font Development Kit for OpenType    
    # The ufo2fdk python bridge:
    try:
        import ufo2fdk
        diagnostics['ufo2fdk'] = True
    except ImportError:
        diagnostics['ufo2fdk'] = False
    # The fdk itself:
    diagnostics['fdk'] = subprocess.Popen(['which','makeotf'], stdout=subprocess.PIPE).communicate()[0].strip()
    # We need both:
    diagnostics['afdko'] = False
    if diagnostics['ufo2fdk'] and diagnostics['fdk']:
        diagnostics['afdko'] = True
    
    return diagnostics

class FontError(Exception):
    """
    Raise nicely verbose errors, should help encourage users in setting
    up a font development workflow.
    """
    def __init__(self, compiler=False,diagnostics=diagnostics()):
        self.compiler = compiler
        self.diagnostics = diagnostics
        self.err = []
    
    def _format(self, text):
        return textwrap.dedent(text)
    
    def fontforge_error(self): 
        if self.diagnostics['fontforge']:
            return """\
            Fontforge appears to be installed an accesible via python.
            """
        elif self.diagnostics['ff']:
            return """\
            FontForge appears to be installed (in %s),
            but the python hooks can’t be found.
            
            Depending on your OS, you might be able to install them
            seperately:
            
            $ sudo apt-get install python-fontforge
            
            Or you might have to reinstall fontforge with the
            --enable-pyextension flag:
            
            brew install fontforge --enable-pyextension
            """ % self.diagnostics['ff']
        else:
            return """\
            Neither FontForge itself nor its python hooks can be found by the 
            build script. This means you will have to install FontForge:

            ubuntu, debian:
            sudo apt-get fontforge python-fontforge

            os x:
            brew install fontforge --enable-pyextension

            More info see:
            openfontlibrary.org/wiki/How_to_install_FontForge"""
    
    def afdko_error(self):
        if self.diagnostics['afdko']:
            return """\
            The AFDKO appears to be installed and accesible via UFO2FDK.
            """
        elif self.diagnostics['ufo2fdk']:
            return """\
            We can find the ufo2fdk bridge but we’re not sure about the 
            AFDKO itself. Please check 
            http://www.adobe.com/devnet/opentype/afdko.html for installation 
            instructions.
            """
        elif self.diagnostics['fdk']:
            return """\
            It appears the AFDKO is installed, but we can’t import the ufo2fdk 
            bridge. Ufo2fdk requires fonttools and robofab. For installation 
            instructions see: http://code.typesupply.com/wiki/ufo2fdk.
            """
        else:
            return """\
            We can’t find the ufo2fdk bridge and we can’t find the
            AFDKO itself either. Please refer to
            http://code.typesupply.com/wiki/ufo2fdk for further
            information."""
    
    def error_message(self):
        if not self.compiler:
            return [self.fontforge_error(), self.afdko_error()]
        elif self.compiler not in known_compilers:
            return ["""\
            You specified an unkown compiler.
            Known compilers are: %s""" %
            ', '.join(self.known_compilers())]
        else:
            err = ["The build script tried to compile with %s" %
            (self.compiler)]
            error = getattr(self, self.compiler + '_error')
            err.append(error())
            if self.compiler == 'afdko':
                if self.diagnostics['fontforge']:
                    err.append('FontForge appears to be working, though.')
                else:
                    err.extend(['You might also want to try out FontForge. It’s free and open source.',self.fontorge_error()])
            return err

    def __str__(self):
        return '\n\n'.join(map(self._format,self.error_message()))

if __name__ == "__main__":
    # This will print diagnostics to stdout
    e = FontError()
    print e