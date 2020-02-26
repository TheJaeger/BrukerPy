#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as op
from glob import glob
import nibabel as nib
import re

class brukerfile():
    """
    This class object serves to hold information on a Bruker subject
    folder. It performs conversion to NifTi and handles BVEC/BVAL file.

    Parameters
    ----------
    path : str
        path to directory containing Bruker acquisitions

    Methods
    -------
    readmethod() :
        returns dictionary of method values

    readreco() :
        returns dictionary of reco values

    Returns
    -------
    none
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
        dict :
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
        dict :
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
                tmp = val.replace('$', '').split('=')
                # Consider when string `val` has a length more than one
                r_dict[tmp[0]] = tmp[1]
        return m_dict

    def brukeracq(self):
        """
        Get Bruker acquisition parameters

        Parameters
        ----------
        self : method object

        Returns
        -------
        DIM: list
            integer list of dimensions in [X, Y, Z, BVALUES, DIRS]
        VOX : list
            float list of voxel size
        NEX : int
            number of repeated experiments (acquisitions)
        NBo : int
            number of B0s in acquition
        bval : list
            list of bvalues in acquisiton
        reco_wordtype : str
            image encoding used in storing Bruker image file
        """
        m_dict = self.readmethod()
        r_dict = self.readreco()

        # Get RECO properties
        fov_xy = [float(x) for x in rmbracket(r_dict['RECO_fov']).split()]
        xy = [int(x) for x in rmbracket(r_dict['RECO_size']).split()]
        DIM = xy + [1, 1]

        if r_dict['RECO_wordtype'] == '_16BIT_SGN_INT':
            reco_wordtype = 'int16'
        elif r_dict['RECO_wordtype'] == '_32BIT_SGN_INT':
            reco_wordtype = 'int32'
        elif r_dict['RECO_wordtype'] == '_8BIT_UNSGN_INT':
            reco_wordtype = 'uint8'
        elif r_dict['RECO_wordtype'] == '_32BIT_FLOAT':
            reco_wordtype = 'single'
        else:
            raise Exception('This acquisition belongs to an unknown '
            'RECO wordtype.')
        
        # Get METHOD properties
        vox_z = float(m_dict['PVM_DwUsedSliceThick'])
        DIM.append(int(m_dict['PVM_DwNDiffDir']))
        NBo = int(m_dict['PVM_DwAoImages'])  # No. of B0s
        bval = [int(x) for x in m_dict['PVM_DwBvalEach'][0].split()]
        DIM[3] = len(bval)
        DIM[2] = int(m_dict['PVM_SPackArrNSlices'][0])
        NEX = int(m_dict['PVM_NRepetitions'])
        VOX = [(f / s) * 10 for f,s in zip(fov_xy, xy)]
        VOX.append(vox_z)
        return DIM VOX NEX NBo bval reco_wordtype

    def getdwgrad(self):
        """
        Returns the diffusion weighted gradient vector table

        Parameters
        ----------
        self : method object

        Returns
        -------
        list : float
            float list of gradient vectors

        """
        m_dict = self.readmethod()
        # Number of experiments
        nex = int(m_dict['PVM_NRepetitions'])
        # Number of diffusion directiosn acquired
        nbvecs = int(m_dict['PVM_DwNDiffDir'])
        # Number of bvals acquired
        nbvals = int(m_dict['PVM_DwAoImages'])
        # bvalues ued for this scan
        bval = [int(s) for s in m_dict['PVM_DwBvalEach'][0].split()]
        # Locate indices of zero-phase images (these are B0s)
        

                
def rmbracket(string):
    """
    Removes brackets and its contents from a string

    Parameters
    ----------
    string: str
        string to remove bracket from

    Returns
    -------
    str :
        string with bracket removed

    Examples
    --------
    >>> myString = 'foo (bar)'
    >>> newString = rmbracket(myString)
    >>> print(newString)
    'foo'
    """
    return re.sub('\(.*?\)','', string)