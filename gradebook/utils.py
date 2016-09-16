# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
from __future__ import print_function

import os
from subprocess import Popen, PIPE
import logging as log
import logging.config

from gradebook import gb_home, class_log
logging.config.fileConfig(os.path.join(gb_home, '.log.conf'),
                          defaults={'logfilename': class_log})


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path, create=False):
        self.new_path = new_path
        if create:
            try: 
                os.makedirs(new_path)
            except OSError:
                if not os.path.isdir(new_path):
                    raise

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)
        log.info('$ cd '+self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def sh(cmd, capture_output=True):
    log.info('$ '+' '.join(cmd))
    print('$ ', ' '.join(cmd))
    try:
        kwargs = {}
        if capture_output:
            kwargs = {'stdout':PIPE, 'stderr':PIPE}
        p = Popen(cmd, **kwargs)
        stdout, stderr = p.communicate()
        if stdout:
            log.info(stdout)
            print(stdout)
        if stderr:
            log.error(stderr)
    except Exception as exc:
        log.warn("error while processing item: %s", exc)

