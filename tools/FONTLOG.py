#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
The FONTLOG is SIL’s concept of a chancelog for a font. When doing a release, 
we generate one automatically based on AUTHORS.txt, README.txt and the 
repository history.

An example of a FONTLOG:
http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&item_id=OFL-FAQ_web#11bc4f28
(pretty url’s wouldn’t hurt the SIL)

We use a line-width of 82 because I manually wrapped my commit messages to 78, 
and git indents them with 4 spaces. These lines stay like they are, and 
unwrapped commit messages get wrapped to the same width.
"""

from textwrap import fill, TextWrapper
from subprocess import Popen, PIPE
import sys

# Get the data

try:
    README = open('README.txt')
except IOError:
    README = open('../README.txt')

try:
    AUTHORS = open('AUTHORS.txt')
except IOError:
    AUTHORS = open('../AUTHORS.txt')

LOG = Popen(['git','log','--reverse'], stdout=PIPE)

# Setup TextWrap instances

wrapper = TextWrapper(width=82)
commit_msg_wrapper = TextWrapper(subsequent_indent='    ', width=82)

# Print FONTLOG to stdout

for line in README:
    print wrapper.fill(line)

print ""
print "____"
print ""
print "Designers:"
print ""
print AUTHORS.read()

print ""
print "____"
print ""
print "Changelog:"
print ""

for line in LOG.stdout:
    if len(line) > 82:
        print commit_msg_wrapper.fill(line)
    else:
        print line,

