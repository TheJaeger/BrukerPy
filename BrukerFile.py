#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as op
import pydicom as pyd

class brukerfile():
    """
    This class object serves to hold information on a Bruker subject
    folder. It performs conversion to NifTi and handles BVEC/BVAL file.

    Parameters
    ----------

    Methods
    -------

    Methods
    -------

    """

    def __init__(self, path):
        if not op.exists(path):
            raise IOError('Input path does not exist, please ensure the '
                          'input path provided is valid.')
