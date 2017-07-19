# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import sys
import csv
import logging
from fabric.api import get
from fabric.api import env
from fabric.api import hide
from fabric.api import put
from fabric.api import sudo
from fabric.api import run
from fabric.decorators import task
from fabric.api import settings
from fabric.colors import green
from fabric.colors import red
from fabric.colors import yellow
from fabric.colors import blue
from fabric.colors import magenta
from datetime import datetime
from fabric.operations import local as lrun


__date__ = "07/19/2017"
__author__ = "Curtis Gortz"
__copyright__ = "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"
__credits__ = ["Curtis Gortz"]
__license__ = "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"
__version__ = "0.1.1"
__maintainer__ = "Curtis Gortz"
__email__ = "curtis.gortz@gmail.com"
__status__ = "Production"


TIMENOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
UTCTIMENOW = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
env.use_ssh_config = True


class StreamToLogger(object):
    """
    Fake streaming to STDOUT to Python native logging
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


@task
def read_hosts_csv(**kwargs):
    """
    Python Farbic CSV Task:Role command line orchestrated workflow
    :param kwargs: Delimiter
    :return: Fabric Role Definitions List
    """
    reader = csv.reader(sys.stdin, **kwargs)
    for row in reader:
        host, role = row
        env.roledefs[role] = env.roledefs.get(role, []) + [host]