#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads method file and generates properties dictionary
"""

def readmethod(path):
    """
    Reads method file from Bruker acquisition.

    Parameters
    ----------
    path : str
        absolute path to Bruker method file

    Returns
    -------
    dict :
        list of method file key-value pairs
    """
    with open(path, mode='r', encoding='ascii') as f:
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

def genmethod(m_dict):
    """
    Generates dictionary list of method variables in appropriate
    format

    Parameters
    ----------
    m_dict : dict
        dictionary returned from readmethod(path)

    Returns
    -------
    dict :
        formatted method dictionary
    """
    methodkeys = getmethodkeys()
    method = {}
    for prop in methodkeys:
        if prop in m_dict:
            # If value from dict is a list
            prop_val = m_dict[prop]
            if isinstance(prop_val, list):
                if len(prop_val) == 1:
                    try:
                        val = convertstring(prop_val[0])
                    except:
                        val = 'Failed list one'
                else:
                    try:
                        val = [convertstring(s) for s in prop_val]
                    except:
                        val = 'Failed list more than one'
                method[prop] = val
            elif isinstance(prop_val, str):
                try:
                    val = convertstring(prop_val)
                except:
                    val = 'Failed string'
                method[prop] = val
            else:
                pass

        else:
            continue
    return method

def convertstring(input):
    """
    Converts a string into list of appropriate types

    Parameters
    ----------
    input : string
        list of str

    Returns
    -------
    out : list
        list of appropriate type
    """
    if not isinstance(input, str):
        raise Exception('Input type is not a string')
    input = input.split()
    try:
        out = [int(s) for s in input]
    except:
        try:
            out = [float(s) for s in input]
        except:
            try:
                out = [str(s) for s in input]
            except:
                print('Unsupported variable type encountered in '
                      'input list.')
    if out and len(out) == 1:
        out = out[0]
    return out

def getmethodkeys():
    """
    Returns a list of all possible method keys

    Parameters
    ----------
    none

    Returns
    -------
    list :
        string list of all keys
    """
    return [
        'Method',
        'EchoTime',
        'PVM_MinEchoTime',
        'NSegments',
        'PVM_RepetitionTime',
        'PackDel',
        'PVM_NAverages',
        'PVM_NRepetitions',
        'PVM_ScanTimeStr',
        'SignalType',
        'PVM_UserType',
        'PVM_DeriveGains',
        'PVM_EncUseMultiRec',
        'PVM_EncActReceivers',
        'PVM_EncZfRead',
        'PVM_EncPpiAccel1',
        'PVM_EncPftAccel1',
        'PVM_EncPpiRefLines1',
        'PVM_EncZfAccel1',
        'PVM_EncOrder1',
        'PVM_EncStart1',
        'PVM_EncMatrix',
        'PVM_EncSteps1',
        'PVM_EncCentralStep1',
        'PVM_EncTotalAccel',
        'PVM_EncNReceivers',
        'PVM_EncAvailReceivers',
        'PVM_EncChanScaling',
        'PVM_OperationMode',
        'ExcPulseEnum',
        'ExcPulse',
        'RefPulseEnum',
        'RefPulse',
        'PVM_GradCalConst',
        'PVM_Nucleus1Enum',
        'PVM_Nucleus1',
        'PVM_RefAttMod1',
        'PVM_RefAttCh1',
        'PVM_RefAttStat1',
        'PVM_Nucleus2Enum',
        'PVM_Nucleus3Enum',
        'PVM_Nucleus4Enum',
        'PVM_Nucleus5Enum',
        'PVM_Nucleus6Enum',
        'PVM_Nucleus7Enum',
        'PVM_Nucleus8Enum',
        'RephaseTime',
        'PVM_EffSWh',
        'PVM_EpiNavigatorMode',
        'PVM_EpiPrefixNavYes',
        'PVM_EpiGradSync',
        'PVM_EpiRampMode',
        'PVM_EpiRampForm',
        'PVM_EpiRampComp',
        'PVM_EpiNShots',
        'PVM_EpiEchoPosition',
        'PVM_EpiRampTime',
        'PVM_EpiSlope',
        'PVM_EpiEffSlope',
        'PVM_EpiBlipTime',
        'PVM_EpiSwitchTime',
        'PVM_EpiEchoDelay',
        'PVM_EpiModuleTime',
        'PVM_EpiGradDwellTime',
        'PVM_EpiAutoGhost',
        'PVM_EpiAcqDelayTrim',
        'PVM_EpiBlipAsym',
        'PVM_EpiReadAsym',
        'PVM_EpiReadDephTrim',
        'PVM_EpiEchoTimeShifting',
        'PVM_EpiEchoShiftA',
        'PVM_EpiEchoShiftB',
        'PVM_EpiDriftCorr',
        'PVM_EpiGrappaThresh',
        'PVM_EpiEchoSpacing',
        'PVM_EpiEffBandwidth',
        'PVM_EpiDephaseTime',
        'PVM_EpiDephaseRampTime',
        'PVM_EpiPlateau',
        'PVM_EpiAcqDelay',
        'PVM_EpiInterTime',
        'PVM_EpiReadDephGrad',
        'PVM_EpiReadOddGrad',
        'PVM_EpiReadEvenGrad',
        'PVM_EpiPhaseDephGrad',
        'PVM_EpiPhaseRephGrad',
        'PVM_EpiBlipOddGrad',
        'PVM_EpiBlipEvenGrad',
        'PVM_EpiPhaseEncGrad',
        'PVM_EpiPhaseRewGrad',
        'PVM_EpiNEchoes',
        'PVM_EpiEchoCounter',
        'PVM_EpiRampUpIntegral',
        'PVM_EpiRampDownIntegral',
        'PVM_EpiBlipIntegral',
        'PVM_EpiSlopeFactor',
        'PVM_EpiSlewRate',
        'PVM_EpiNSamplesPerScan',
        'PVM_EpiPrefixNavSize',
        'PVM_EpiPrefixNavDur',
        'PVM_EpiNScans',
        'PVM_EpiNInitNav',
        'PVM_EpiAdjustMode',
        'PVM_EpiReadCenter',
        'PVM_EpiPhaseCorrection',
        'PVM_EpiGrappaCoefficients',
        'BwScale',
        'PVM_TrajectoryMeasurement',
        'PVM_UseTrajectory',
        'PVM_ExSliceRephaseTime',
        'SliceSpoilerDuration',
        'SliceSpoilerStrength',
        'PVM_DigAutSet',
        'PVM_DigQuad',
        'PVM_DigFilter',
        'PVM_DigRes',
        'PVM_DigDw',
        'PVM_DigSw',
        'PVM_DigNp',
        'PVM_DigShift',
        'PVM_DigGroupDel',
        'PVM_DigDur',
        'PVM_DigEndDelMin',
        'PVM_DigEndDelOpt',
        'PVM_GeoMode',
        'PVM_SpatDimEnum',
        'PVM_Isotropic',
        'PVM_Fov',
        'PVM_FovCm',
        'PVM_SpatResol',
        'PVM_Matrix',
        'PVM_MinMatrix',
        'PVM_MaxMatrix',
        'PVM_AntiAlias',
        'PVM_MaxAntiAlias',
        'PVM_SliceThick',
        'PVM_ObjOrderScheme',
        'PVM_ObjOrderList',
        'PVM_NSPacks',
        'PVM_SPackArrNSlices',
        'PVM_MajSliceOri',
        'PVM_SPackArrSliceOrient',
        'PVM_SPackArrReadOrient',
        'PVM_SPackArrReadOffset',
        'PVM_SPackArrPhase1Offset',
        'PVM_SPackArrPhase2Offset',
        'PVM_SPackArrSliceOffset',
        'PVM_SPackArrSliceGapMode',
        'PVM_SPackArrSliceGap',
        'PVM_SPackArrSliceDistance',
        'PVM_SPackArrGradOrient',
        'Reco_mode',
        'NDummyScans',
        'PVM_TriggerModule',
        'PVM_TaggingOnOff',
        'PVM_TaggingPulse',
        'PVM_TaggingDeriveGainMode',
        'PVM_TaggingMode',
        'PVM_TaggingDir',
        'PVM_TaggingDistance',
        'PVM_TaggingMinDistance',
        'PVM_TaggingThick',
        'PVM_TaggingOffset1',
        'PVM_TaggingOffset2',
        'PVM_TaggingAngle',
        'PVM_TaggingDelay',
        'PVM_TaggingModuleTime',
        'PVM_TaggingPulseNumber',
        'PVM_TaggingPulseElement',
        'PVM_TaggingGradientStrength',
        'PVM_TaggingSpoilGrad',
        'PVM_TaggingSpoilDuration',
        'PVM_TaggingGridDelay',
        'PVM_TaggingD0',
        'PVM_TaggingD1',
        'PVM_TaggingD2',
        'PVM_TaggingD3',
        'PVM_TaggingD4',
        'PVM_TaggingD5',
        'PVM_TaggingP0',
        'PVM_TaggingLp0',
        'PVM_TaggingGradAmp1',
        'PVM_TaggingGradAmp2',
        'PVM_TaggingGradAmp3',
        'PVM_TaggingGradAmp4',
        'PVM_TaggingSpoiler',
        'PVM_FatSupOnOff',
        'PVM_MagTransOnOff',
        'PVM_FovSatOnOff',
        'PVM_FovSatNSlices',
        'PVM_FovSatSliceOrient',
        'PVM_FovSatThick',
        'PVM_FovSatOffset',
        'PVM_FovSatSliceVec',
        'PVM_SatSlicesPulseEnum',
        'PVM_SatSlicesPulse',
        'PVM_SatSlicesDeriveGainMode',
        'PVM_FovSatGrad',
        'PVM_FovSatSpoilTime',
        'PVM_FovSatSpoilGrad',
        'PVM_FovSatModuleTime',
        'PVM_FovSatFL',
        'PVM_SatD0',
        'PVM_SatD1',
        'PVM_SatD2',
        'PVM_SatP0',
        'PVM_SatLp0',
        'PVM_TriggerOutOnOff',
        'PVM_TriggerOutMode',
        'PVM_TriggerOutDelay',
        'PVM_TrigOutD0',
        'PVM_PreemphasisSpecial',
        'PVM_PreemphasisFileEnum',
        'PVM_EchoTime1',
        'PVM_EchoTime2',
        'PVM_EchoTime',
        'PVM_NEchoImages',
        'EchoRepTime',
        'SegmRepTime',
        'SegmDuration',
        'SegmNumber',
        'PVM_InversionTime',
        'PVM_EchoPosition',
        'SequenceOptimizationMode',
        'EchoPad',
        'RFSpoilerOnOff',
        'SpoilerDuration',
        'SpoilerStrength',
        'NDummyEchoes',
        'Mdeft_PreparationMode',
        'Mdeft_ExcPulseEnum',
        'Mdeft_ExcPulse',
        'Mdeft_InvPulseEnum',
        'Mdeft_InvPulse',
        'Mdeft_PrepDeriveGainMode',
        'Mdeft_PrepSpoilTime',
        'Mdeft_PrepMinSpoilTime',
        'Mdeft_PrepSpoilGrad',
        'Mdeft_PrepModuleTime',
        'PVM_ppgMode1',
        'PVM_ppgFreqList1Size',
        'PVM_ppgFreqList1',
        'PVM_ppgGradAmp1',
        'EffectiveTE',
        'PVM_RareFactor',
        'PVM_SliceBandWidthScale',
        'PVM_ReadDephaseTime',
        'PVM_2dPhaseGradientTime',
        'PVM_EvolutionOnOff',
        'PVM_SelIrOnOff',
        'PVM_FatSupprPulseEnum',
        'PVM_FatSupprPulse',
        'PVM_FatSupDeriveGainMode',
        'PVM_FatSupBandWidth',
        'PVM_FatSupSpoilTime',
        'PVM_FatSupSpoilGrad',
        'PVM_FatSupModuleTime',
        'PVM_FatSupFL',
        'PVM_FsD0',
        'PVM_FsD1',
        'PVM_FsD2',
        'PVM_FsP0',
        'PVM_InFlowSatOnOff',
        'PVM_InFlowSatNSlices',
        'PVM_InFlowSatThick',
        'PVM_InFlowSatGap',
        'PVM_InFlowSatSide',
        'PVM_FlowSatPulse',
        'PVM_FlowSatDeriveGainMode',
        'PVM_InFlowSatSpoilTime',
        'PVM_InFlowSatSpoilGrad',
        'PVM_InFlowSatModuleTime',
        'PVM_SfD0',
        'PVM_SfD1',
        'PVM_SfD2',
        'PVM_SfP0',
        'PVM_SfLp0',
        'PVM_MotionSupOnOff',
        'PVM_FlipBackOnOff',
        'PVM_MotionSupOnOff',
        'EchoTimeMode',
        'ReadSpoilerDuration',
        'ReadSpoilerStrength',
        'PVM_MovieOnOff',
        'PVM_NMovieFrames',
        'TimeForMovieFrames',
        'PVM_BlBloodOnOff',
        'PVM_ppgFlag1',
        'RECO_wordtype',
        'RECO_map_mode',
        'RECO_map_percentile',
        'RECO_map_error',
        'RECO_map_range'
    ]
