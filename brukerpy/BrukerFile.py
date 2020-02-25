#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as op
from glob import glob
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
            raise IOError('Input path does not exist, please ensure '
            'the input path provided is valid.')
        if not op.isdir(path):
            raise IOError('It appears that the is not a directory. '
            'BrukerPu currently only support a Bruekr directory as '
            'an input.')
        brukerPaths = {
            'method': glob(op.join(path, '**', '*method'), recursive=True)[0],
            'reco': glob(op.join(path, '**', '*reco'), recursive=True)[0],
            '2dseq': glob(op.join(path, '**', '*2dseq'), recursive=True)[0],
            'acqp': glob(op.join(path, '**', '*acqp'), recursive=True)[0]
        }
        for key in brukerPaths:
            if op.exists(key):
                raise IOError('Bruker {} file not found. Please '
                'ensure that the file exists at {}', format(key,
                brukerPaths[key]))
        self.method = brukerPaths['method']
        self.reco = brukerPaths['reco']
        self.seq = brukerPaths['2dseq']
        self.acqp = brukerPaths['acqp']

    def readmethod(self):
        """
        Reads method file from Bruker acquisition.

        Parameters
        ----------
        self: method object

        Returns
        -------
        dict
            list of method file key-value pairs
        """"
        with open(method, mode='r', encoding='ascii') as f:
            data = f.read()
        data = data.split('##')
        data = [x.splitlines() for x in data]
        m_dict = {}
        for val in data:
            if val:
                val = [s.replace('$', '') for s in val]
                tmp = val[0].split('=')
                # Consider when string `val` has a length more than one
                if len(val) > 1:
                    m_dict[tmp[0]] = val[1:]
                elif len(val) == 1:
                    m_dict[tmp[0]] = tmp[1]
        return m_dict

    def readreco(self):
        """
        Reads reco file from Bruker acquisition.

        Parameters
        ----------
        self: method object

        Returns
        -------
        dict
            list of reco file key-value pairs
        """"
        with open(reco, mode='r', encoding='ascii') as f:
            data = f.read()
        data = data.split('##')
        data = [s.replace('#', '') for s in data]
        data = [s.replace('$', '') for s in data]
        data = [s.replace('\n', '') for s in data]
        r_dict = {}
        for val in data:
            if val:
                val = [s.replace('$', '') for s in val]
                tmp = val[0].split('=')
                # Consider when string `val` has a length more than one
                if len(val) > 1:
                    m_dict[tmp[0]] = val[1:]
                elif len(val) == 1:
                    m_dict[tmp[0]] = tmp[1]
        return m_dict

                


