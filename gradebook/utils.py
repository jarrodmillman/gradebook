# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from subprocess import Popen, PIPE
import logging as log
import logging.config

from gradebook import gb_home, class_log
logging.config.fileConfig(os.path.join(gb_home, '.log.conf'),
                          defaults={'logfilename': class_log})


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath, create=False):
        self.newPath = newPath
        if create:
            try: 
                os.makedirs(newPath)
            except OSError:
                if not os.path.isdir(newPath):
                    raise

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
        log.info('$ cd '+self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def sh(cmd):
    log.info('$ '+' '.join(cmd))
    print '$ ', ' '.join(cmd)
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            log.info(stdout)
            print stdout
        if stderr:
            log.error(stderr)
    except Exception, exc:
        log.warn("error while processing item: %s", exc)

