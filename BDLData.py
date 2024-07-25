import pandas as pd
from pprint import pprint
from BD_data import BD, BD_ML, getBDLs
from createCSV import main as mainBigData
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
    gitData = {}
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
        gitData[bdl.name] = regionPerBDL
    return gitData


def justToKnowIfItsWorking():
    actualBigAssData = mainBigData(1, 1)
    rawData = pd.read_csv('rawData.csv')
    for column2compare in rawData['Requirements'].unique():
        if column2compare not in ['CKAs imperfect orders', 'CKAs B cancellation rate', 'Promotion quality', 'Promotional Coverage']:
            sumaTotal = [0, 0, 0, 0, 0, 0, 0, 0]
            for bdl_name, importantStuff in actualBigAssData.items():
                for key, dictOfColumns in importantStuff.items():
                    for column, listOfValues in dictOfColumns.items():
                        if column == column2compare:
                            for i, value in enumerate(listOfValues):
                                try:
                                    if value == 'TBD':
                                        continue
                                    sumaTotal[i] += float(value)
                                except:
                                    print('bdl_name', bdl_name)
                                    print('key', key)
                                    print('column ' + '"'+column+'"')
                                    print('listOfValues', listOfValues)
                                    print('value', value)
                                    raise Exception('Error')
            print('"'+column2compare+'"')
            print(rawData[rawData['Requirements'] == column].values[0][1:])
            print(sumaTotal)


# pprint(getBasicData())
justToKnowIfItsWorking()
