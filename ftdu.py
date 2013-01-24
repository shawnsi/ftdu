#!/usr/bin/env python

import gevent
import os
import sys
import magic
from hurry.filesize import size as human_size

path = sys.argv[1]
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

for root, dirs, files in os.walk(path):
    for filename in files:
        filepath = os.path.join(root, filename)
        if not os.path.islink(filepath):
            current_file = filepath
            filetype = magic.from_file(filepath).split(',')[0]
            filesize = os.path.getsize(filepath)
            total = totals.setdefault(filetype, 0)
            totals[filetype] = total + filesize
            total_bytes += filesize
        gevent.sleep()

status()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

