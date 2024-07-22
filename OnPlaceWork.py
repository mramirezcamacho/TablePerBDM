import pandas as pd


class BD():
    def __init__(self, name, bd_type):
        self.name = name
        self.bd_type = bd_type
        self.cities = {}
        self.roles = []
        self.RsTypes = []

    def addCity(self, country, city):
        if country not in self.cities:
            self.cities[country] = []
        if city not in self.cities[country]:
            self.cities[country].append(city)

    def addRole(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def addRsType(self, RsType):
        if RsType not in self.RsTypes:
            self.RsTypes.append(RsType)

    def __str__(self) -> str:
        cities_str = "\n".join(f"{country}: {', '.join(
            cities)}" for country, cities in self.cities.items())
        return f"{self.name} ({self.bd_type}):\nRoles: {', '.join(self.roles)}\nRsTypes: {', '.join(self.RsTypes)}\nCities:\n{cities_str}"


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


def citiesPerBDM():
    MX_Data, MAC_Data, PE_Data = getBasicData()
    basicDataDict = {'MX': MX_Data, 'MAC': MAC_Data, 'PE': PE_Data}
    BDM_MX, BDM_MAC, BDM_PE, BDL_MX, BDL_MAC, BDL_PE = getBDM_BDL()
    BDMS_data = {'MX': BDM_MX, 'MAC': BDM_MAC, 'PE': BDM_PE}
    BDLS_data = {'MX': BDL_MX, 'MAC': BDL_MAC, 'PE': BDL_PE}
    bigData = {'BDM': BDMS_data, 'BDL': BDLS_data}

    bds = []
    for BdType, bigDatita in bigData.items():
        for key, value in bigDatita.items():
            for bdm in value:
                bdmObject = BD(bdm, BdType)
                basicData = basicDataDict[key]
                if 'Support city' in basicData.columns:
                    cities = basicData[basicData[BdType]
                                       == bdm][['Country', 'Support city']]
                else:
                    cities = basicData[basicData[BdType]
                                       == bdm][['Country', 'Support City']]
                roles = basicData[basicData[BdType] == bdm]['Role'].unique()
                RsType = basicData[basicData[BdType]
                                   == bdm]['Vertical'].unique()
                for index, row in cities.iterrows():
                    country = row['Country']
                    if 'Support city' in basicData.columns:
                        city = row['Support city']
                    else:
                        city = row['Support City']
                    bdmObject.addCity(country, city)
                for rol in roles:
                    bdmObject.addRole(rol)
                for RsType in RsType:
                    bdmObject.addRsType(RsType)
                bds.append(bdmObject)
    return bds


bds = citiesPerBDM()
for bd in bds:
    if bd.name == 'marcorojas':
        print(bd)

# Toca dividir los porcentajes por BD's, no por BDM's
# Tabla por cabeza de farmer y hunter si tiene ambas un BDM-BDL
