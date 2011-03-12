#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists, join
from robofab.objects.objectsRF import RFont
import codecs
"""
When the README.txt or the COPYING-OFL.txt is updated, we want to have that 
information also updated in the UFO metadata, fontinfo.plist.
"""

def c_open(filename):
    return codecs.open(filename, "r", "utf-8")

def contents(filename):
    """
    Tries several paths in which the necessary files could be located
    (Depending on if the file is run from the Rakefile or the tools folder)
    """
    try:
        f = c_open(filename)
    except IOError:
        try:
            f = c_open(join('..',filename))
        except IOError:
            f = c_open(join('tools',filename))
    return f.read()

def update_metadata(font):
    """
    The license bundled with the font is linewrapped. We don’t want these 
    linewraps in the metadata because font programs have dialog boxes that 
    might have another width.
    
    We leave the copyright statements in COPYING-OFL.txt as they are, but swap 
    the license text with an unlinewrapped version.
    
    README.txt is currently not linewrapped and can be embedded as is.
    """
    if exists(font):
        font_location = font
    else:
        font_location = join('..',font)
        
    font = RFont(font_location)
    
    information = contents('README.txt')
    # print information
    font.info.note = information
    
    f = contents('COPYING-OFL.txt')
    preamble = u"""The Open Baskerville font files are dual-licensed under the GNU GPL version 3 (GNU General Public License) and the SIL Open Font License (OFL). See 'COPYING-GPLv3.txt' and 'COPYING-OFL.txt' respectively. There is also a FAQ on the OFL (see 'COPYING-OFL-FAQ.txt').

What follows is the text of the SIL Open Font License.
___

"""
    copyright = f   .split('-----------------------------------------------------------')[0]
    ofl = contents('OFL-nolinewrap')
    license = preamble + copyright + ofl
    # print license
    font.info.openTypeNameLicense = license
    
    font.save()

if __name__ == "__main__":
    update_metadata('OpenBaskerville.ufo')
