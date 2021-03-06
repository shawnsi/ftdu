#!/usr/bin/env python
'''File Type Disk Usage.

Usage:
    ftdu.py [-v] <path>

Options:
    -v --verbose    Show verbose libmagic types.

'''

from docopt import docopt
import gevent
import os
import sys
import magic
from hurry.filesize import size as human_size

args = docopt(__doc__, version='File Type Disk Usage 1.0')

count = 0
current_file = ''
total_bytes = 0
totals = {}

def spawn_interval(f, interval=1, *args, **kwargs):
    '''
    Spawns a new greenlet on a given interval until the main loop exits.

    Args:

        f - the function to wrap in greenlets

    Keyword Args:

        interval - number of seconds to wait between running each greenlet

    Example:

        def run_me():
            return True

        # Run the function every 5 seconds
        spawn_interval(run_me, interval=5)
    '''
    gevent.spawn(f, *args, **kwargs)
    gevent.spawn_later(interval, spawn_interval, f, interval, *args, **kwargs)

def status():
    os.system('clear')
    if current_file:
        print 'Current file: %s' % current_file
        print 'Files processed: %d' % count
        print 'Total data: %s' % human_size(total_bytes)
        print

    total_tuples = sorted(totals.items(), key=lambda i: i[1], reverse=True)
    top25 = total_tuples[:25]
    print 'Top %d file types by size:' % len(top25)
    for (filetype, size) in top25:
        try:
            percent = size / float(total_bytes)
        except ZeroDivisionError:
            percent = 0

        print '%s: %.2f%%' % (filetype, percent * 100)

spawn_interval(status)

# Walk all files in all subdirectories of the path
for root, dirs, files in os.walk(args['<path>']):
    for filename in files:
        filepath = os.path.join(root, filename)
        # We ignore symlinks because getsize returns the target file size
        if not os.path.islink(filepath):
            current_file = filepath
            filetype = magic.from_file(filepath)
            if not args['--verbose']:
                filetype = filetype.split(',')[0]
            filesize = os.path.getsize(filepath)
            total = totals.setdefault(filetype, 0)
            totals[filetype] = total + filesize
            total_bytes += filesize
            count += 1
        gevent.sleep()

status()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

