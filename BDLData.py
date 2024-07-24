import pandas as pd
from pprint import pprint
from BD_data import BD, BD_ML, getBDLs
import os


def prettifyName(name):
    name = name.replace('á', 'a').replace('é', 'e').replace(
        'í', 'i').replace('ó', 'o').replace('ú', 'u')
    if name == 'Bogota, D.C.':
        return 'Bogota D.C.'
    if name == 'Juarez(CHIH)':
        return 'Juarez CHIH'
    return name


def getCityRegionData():
    dfRegion = pd.read_csv('MX_city_region.csv')
    return dfRegion


def getBasicData():
    bdls = getBDLs()
    cityRegion = getCityRegionData()
    for bdl in bdls:
        regionPerBDL = {}
        for country, listOfCities in bdl.cities(organized=True).items():
            for city in listOfCities:
                if country == 'MX':
                    city = prettifyName(city)
                    region = cityRegion[cityRegion['city_name']
                                        == city]['region'].values[0]
                    if country not in regionPerBDL:
                        regionPerBDL[country] = []
                    if region not in regionPerBDL[country]:
                        regionPerBDL[country].append(region)
                else:
                    city = prettifyName(city)
                    if country not in regionPerBDL:
                        regionPerBDL[country] = []
                    if city not in regionPerBDL[country]:
                        regionPerBDL[country].append(city)
        print(bdl.name)
        print(regionPerBDL)
        print()


getBasicData()
