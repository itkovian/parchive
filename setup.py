#!/usr/bin/env python
# -*- coding: latin-1 -*-
##
# Copyright 2019-2019 Ghent University
#
# This file is part of parchive.
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# the Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# All rights reserved.
#
##
"""
parchive base distribution setup.py

@author: Andy Georges (Ghent University)
"""
import vsc.install.shared_setup as shared_setup
from vsc.install.shared_setup import ag

PACKAGE = {
    'version': '0.0.1',
    'author': [ag],
    'maintainer': [ag],
    'install_requires': [
        'vsc-base >= 2.4.16',
        'future >= 0.16.0',
    ],
}


if __name__ == '__main__':
    shared_setup.action_target(PACKAGE)
