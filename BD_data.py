import pandas as pd
from pprint import pprint


class BD():
    def __init__(self, name, city, role, RsType, country):
        self.name = name
        self.city = city
        self.role = role
        self.RsType = RsType
        self.country = country


class BD_ML():
    def __init__(self, name, bd_type):
        self.name = name
        self.bd_type = bd_type
        self.bds = []

    def addBD(self, bd):
        self.bds.append(bd)

    def cities(self):
        cities = {}
        for bd in self.bds:
            if bd.city not in cities:
                cities[bd.city] = 1
            else:
                cities[bd.city] += 1
        return cities

    def roles(self):
        roles = {}
        for bd in self.bds:
            if bd.role not in roles:
                roles[bd.role] = 1
            else:
                roles[bd.role] += 1
        return roles

    def RsTypes(self):
        RsTypes = {}
        for bd in self.bds:
            if bd.RsType not in RsTypes:
                RsTypes[bd.RsType] = 1
            else:
                RsTypes[bd.RsType] += 1
        return RsTypes

    def countries(self):
        countries = {}
        for bd in self.bds:
            if bd.country not in countries:
                countries[bd.country] = 1
            else:
                countries[bd.country] += 1
        return countries

    def indepthInfo(self) -> str:
        cities = self.cities()
        roles = self.roles()
        RsTypes = self.RsTypes()
        countries = self.countries()
        return f'Cities: {cities}\nRoles: {roles}\nRsTypes: {RsTypes}\nCountries: {countries}'

    def __str__(self):
        return f'{self.name} - {self.bd_type}'


def getBasicData():
    MX = 'MX.csv'
    MAC = 'MAC.csv'
    PE = 'PE.csv'
    MX_Data = pd.read_csv(MX)
    MAC_Data = pd.read_csv(MAC)
    PE_Data = pd.read_csv(PE)
    return MX_Data, MAC_Data, PE_Data


def getBDM_BDL():
    MX_Data, MAC_Data, PE_Data = getBasicData()
    BDM_MX = MX_Data['BDM'].unique()
    BDM_MAC = MAC_Data['BDM'].unique()
    BDM_PE = PE_Data['BDM'].unique()
    BDL_MX = MX_Data['BDL'].unique()
    BDL_MAC = MAC_Data['BDL'].unique()
    BDL_PE = PE_Data['BDL'].unique()
    return BDM_MX, BDM_MAC, BDM_PE, BDL_MX, BDL_MAC, BDL_PE


def mxCityData():
    mxCity = pd.read_csv('MX_city_region.csv')
    return mxCity


def citiesPerBDM() -> list:
    MX_Data, MAC_Data, PE_Data = getBasicData()
    basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data, 'PE': PE_Data}
    BDM_MX, BDM_MAC, BDM_PE, BDL_MX, BDL_MAC, BDL_PE = getBDM_BDL()
    BDMS_data = {'MX': BDM_MX, 'MAC': BDM_MAC, 'PE': BDM_PE}
    BDLS_data = {'MX': BDL_MX, 'MAC': BDL_MAC, 'PE': BDL_PE}
    bigData = {'BDM': BDMS_data, 'BDL': BDLS_data}

    bds = []
    for BdType, bigDatita in bigData.items():
        for country, value in bigDatita.items():
            for bdm in value:
                bd_ML = BD_ML(bdm, BdType)
                bdmData = basicDataDict[country][basicDataDict[country]
                                                 [BdType] == bdm]
                for index, row in bdmData.iterrows():
                    bd = BD(row['BD Username'],
                            row['Support city'], row['Role'].capitalize(), row['Vertical'], row['Country'])
                    bd_ML.addBD(bd)
                bds.append(bd_ML)
    return bds


bds = citiesPerBDM()
