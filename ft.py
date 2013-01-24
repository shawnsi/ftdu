#!/usr/bin/env python

import os
import sys
import magic

path = sys.argv[1]

for root, dirs, files in os.walk(path):
    for filename in files:
        filepath = os.path.join(root, filename)
        if not os.path.islink(filepath):
            filetype = magic.from_file(filepath).split(',')[0]
            print '%s: %s' % (filepath, filetype)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

