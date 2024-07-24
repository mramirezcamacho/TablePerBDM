import pandas as pd
from pprint import pprint


class BD():
    def __init__(self, name, city, role, RsType, country):
        self.name = name
        self.city = city
        self.role = role.capitalize()
        self.RsType = RsType
        self.country = country

    def __str__(self):
        return f'{self.name}: de la ciudad de:{self.city}, como {self.role}, para los Rs {self.RsType}, en el país {self.country}'


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

    def paises4role(self):
        answer = {}
        for bd in self.bds:
            key = bd.role[0]+bd.RsType
            if key not in answer:
                answer[key] = []
            if bd.country not in answer[key]:
                answer[key].append(bd.country)
        return answer

    def calculateDistribution(self):
        distribution = {}
        for bd in self.bds:
            key2save = f'{bd.RsType}_{bd.country}_{bd.city}_{bd.role}'
            if key2save not in distribution:
                distribution[key2save] = 1
            else:
                distribution[key2save] += 1
        return distribution

    def cities(self, country=None, organized=False):
        cities = {}
        for bd in self.bds:
            if country is None:
                if not organized:
                    if bd.city not in cities:
                        cities[bd.city] = 1
                    else:
                        cities[bd.city] += 1
                else:
                    if bd.country not in cities:
                        cities[bd.country] = []
                    if bd.city not in cities[bd.country]:
                        cities[bd.country].append(bd.city)
            else:
                if bd.country == country:
                    if bd.city not in cities:
                        cities[bd.city] = 1
                    else:
                        cities[bd.city] += 1
        return cities

    def calculateDistribution4search(self):
        distri = {}
        for bd in self.bds:
            typeRS = bd.RsType
            country = bd.country
            city = bd.city
            role = bd.role
            if typeRS not in distri:
                distri[typeRS] = {}
            if role not in distri[typeRS]:
                distri[typeRS][role] = {}
            if country not in distri[typeRS][role]:
                distri[typeRS][role][country] = {}
            if city not in distri[typeRS][role][country]:
                distri[typeRS][role][country][city] = 1
            else:
                distri[typeRS][role][country][city] += 1
        return distri

    def organizarDistribution(self):
        distribution = self.calculateDistribution()
        newDistr = {}
        for key, value in distribution.items():
            try:
                RsType, country, city, role = key.split('_')
            except:
                print(key)
                raise ValueError
            newR = role[0]
            key2search = f'{newR}{RsType}'
            if key2search not in newDistr:
                newDistr[key2search] = {}
            if country not in newDistr[key2search]:
                newDistr[key2search][country] = {}
            if city not in newDistr[key2search][country]:
                newDistr[key2search][country][city] = value
            else:
                newDistr[key2search][country][city] += value
        return newDistr

    def __str__(self):
        return f'{self.name} _ {self.bd_type}'


def distributionOfBDsPerCountryPerRolePerOrganization():
    # MX_Data, MAC_Data, PE_Data = getBasicData()
    MX_Data, MAC_Data = getBasicData()
    # basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data, 'PE': PE_Data}
    basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data, }
    distribution: dict = {}
    for country, data in basicDataDict.items():
        for i, row in data.iterrows():
            country = row['Country']
            role = row['Role']
            organization = row['Vertical']
            city = row['Support city']
            key2save = f'{organization}_{country}_{city}_{role}'
            if key2save not in distribution:
                distribution[key2save] = 1
            else:
                distribution[key2save] += 1
    return distribution


def getBasicData():
    MX = 'MX.csv'
    MAC = 'MAC_PE.csv'
    # PE = 'PE.csv'
    MX_Data = pd.read_csv(MX)
    MAC_Data = pd.read_csv(MAC)
    # PE_Data = pd.read_csv(PE)
    return MX_Data, MAC_Data  # , PE_Data


def getBDM_BDL():
    # MX_Data, MAC_Data, PE_Data = getBasicData()
    MX_Data, MAC_Data = getBasicData()
    BDM_MX = MX_Data['BDM'].unique()
    BDM_MAC = MAC_Data['BDM'].unique()
    # BDM_PE = PE_Data['BDM'].unique()
    BDL_MX = MX_Data['BDL'].unique()
    BDL_MAC = MAC_Data['BDL'].unique()
    # BDL_PE = PE_Data['BDL'].unique()
    # return BDM_MX, BDM_MAC, BDM_PE, BDL_MX, BDL_MAC, BDL_PE
    return BDM_MX, BDM_MAC, BDL_MX, BDL_MAC


def mxCityData():
    mxCity = pd.read_csv('MX_city_region.csv')
    return mxCity


def citiesPerBDM() -> list:
    # MX_Data, MAC_Data, PE_Data = getBasicData()
    MX_Data, MAC_Data = getBasicData()
    # basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data, 'PE': PE_Data}
    basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data}
    # BDM_MX, BDM_MAC, BDM_PE, BDL_MX, BDL_MAC, BDL_PE = getBDM_BDL()
    BDM_MX, BDM_MAC, BDL_MX, BDL_MAC = getBDM_BDL()
    # BDMS_data = {'MX': BDM_MX, 'MAC': BDM_MAC, 'PE': BDM_PE}
    BDMS_data = {'MX': BDM_MX, 'MAC': BDM_MAC, }
    # BDLS_data = {'MX': BDL_MX, 'MAC': BDL_MAC, 'PE': BDL_PE}
    BDLS_data = {'MX': BDL_MX, 'MAC': BDL_MAC, }
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


def getBDLs():
    bds = citiesPerBDM()
    bdl = []
    for bd in bds:
        if bd.bd_type == 'BDL':
            bdl.append(bd)
    return bdl
