import pandas as pd
import pprint as pp


def getData():
    BMD_BML = pd.read_csv('BDM_BDL_SSL.csv')
    MX = pd.read_csv('MX.csv')
    MAC = pd.read_csv('MAC.csv')
    PE = pd.read_csv('PE.csv')
    # Filtering the DataFrame
    BDMs = BMD_BML[BMD_BML['Position'].str.contains('BDM')]
    BML = BMD_BML[BMD_BML['Position'] == 'BD lead']
    return BDMs, BML, MX, MAC, PE


def getBDMsNames():
    BDMs, BML, MX, MAC, PE = getData()
    MX_BDM = MX['BDM'].unique()
    MX_BDM_sorted = sorted(MX_BDM)

    BDMs_MX = BDMs[BDMs['Country'] == 'MX']
    BDMS_Names = BDMs_MX['BDM/BDC Username'].unique()
    BDMS_Names_sorted = sorted(BDMS_Names)
    return MX_BDM_sorted, BDMS_Names_sorted


def discrepancias():
    MX_BDM_sorted, BDMS_Names_sorted = getBDMsNames()
    MX_BDM_set = set(MX_BDM_sorted)
    BDMS_Names_set = set(BDMS_Names_sorted)

    # Find differences and intersection
    only_in_MX = MX_BDM_set - BDMS_Names_set
    only_in_BDMS = BDMS_Names_set - MX_BDM_set
    in_both = MX_BDM_set & BDMS_Names_set

    # Print results
    print("Only in MX:")
    pp.pprint(sorted(only_in_MX))

    print("\nOnly in BDMs:")
    pp.pprint(sorted(only_in_BDMS))

    print("\nIn both:")
    pp.pprint(sorted(in_both))


discrepancias()
