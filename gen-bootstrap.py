#!/usr/bin/env python

import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'pip'),
                    'install', 'gevent'])
    subprocess.call([join(home_dir, 'bin', 'pip'),
                    'install', 'python-magic'])
    subprocess.call([join(home_dir, 'bin', 'pip'),
                    'install', 'hurry.filesize'])
"""))
print output

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

