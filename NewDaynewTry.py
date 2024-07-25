import csv
import os
from pprint import pprint
import pandas as pd


def getColumns(ForH='Both', organization='Both'):
    allCKA = ['Daily Orders CKA', 'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024', 'CKA # of R1s  (5+ Daily Orders)', 'CKAs B cancellation rate', 'CKAs imperfect orders',
              'CKA Meal Loss % GMV', 'CKA B App orders on time rate', 'CKA # Orders CDMX', 'CKA # Orders BOG', 'CKA # Orders MED', 'Promotional Coverage', 'Promotion quality']

    allSME = ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
              'SME Meal Loss % GMV', 'SME B App orders on time rate', 'SME # Orders CDMX', 'SME # Orders MTY', 'SME # Orders GDL', 'SME # Orders BOG', 'SME # Orders MED', 'Promotional Coverage', 'Promotion quality']

    exclusions = ['Promotional Coverage', 'Promotion quality']

    # Filter out elements from allCKA and allSME lists based on exclusions
    allCKA = [item for item in allCKA if item not in exclusions]
    allSME = [item for item in allSME if item not in exclusions]

    if ForH == 'Both' and organization == 'Both':
        return allCKA, allSME
    if organization == 'CKA':
        if ForH == 'Both':
            return allCKA
    else:
        if ForH == 'Both':
            return allSME


def miniColumnaPerCountry(country, region=None, all=False):
    if all:
        return ['CO  - Baseline', 'CO  - Target', 'MX - Baseline', 'MX - Target', 'CR  - Baseline', 'CR  - Target', 'PE  - Baseline', 'PE  - Target', 'Norte - Baseline', 'Norte - Target', 'CDMX - Baseline', 'CDMX - Target', 'Pacifico - Baseline', 'Pacifico - Target', 'Sur - Baseline', 'Sur - Target']
    if country == 'CO':
        return ['CO  - Baseline', 'CO  - Target']
    if country == 'CR':
        return ['CR  - Baseline', 'CR  - Target']
    if country == 'PE':
        return ['PE  - Baseline', 'PE  - Target']
    if country == 'MX':
        if region != None:
            return [f'{region} - Baseline', f'{region} - Target', 'MX - Baseline', 'MX - Target']
        else:
            return ['MX - Baseline', 'MX - Target']
    return None


def personResponsabilitiesBigNames(person: str):
    data = {
        'catalinaarteaga': {
            'paises': ['MX', 'CO', 'PE', 'CR',],
            'divisiones': {'CKA': getColumns(organization='CKA'),
                           'SME': getColumns(organization='SME')}
        },
        'patriciacatalunadiaz': {
            'paises': ['CO', 'PE', 'CR',],
            'divisiones': {'CKA': getColumns(organization='CKA'),
                           'SME': getColumns(organization='SME')}
        },
        'tomasjaramillo': {
            'paises': ['MX',],
            'divisiones': {'CKA':  ['Daily Orders CKA',  'Daily Orders of CKA Rs acquired in 2024', 'CKA # of R1s  (5+ Daily Orders)', 'CKAs B cancellation rate',
                                    'CKAs imperfect orders', 'CKA Meal Loss % GMV', 'CKA B App orders on time rate',], }
        },
        'sergiocanal': {
            'paises': ['MX',],
            'divisiones': {'CKA': ['Daily Orders CKA', 'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024',], }
        },
    }
    if person in data:
        return data[person]
    else:
        print('la persona que buscas no existe en esta seccion')
        raise ValueError


def createFolderIfNotExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def createCSVbyList(data: list, fileName: str):
    createFolderIfNotExists('BDL_tables')
    fileName = 'BDL_tables/'+fileName
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def makePrettyBaseNumber(baseNumber):
    if 'k' in baseNumber:
        return float(baseNumber.replace('k', '')) * 1000
    elif baseNumber == 'TBD':
        return 'TBD'
    elif '%' in baseNumber:
        return baseNumber
    return float(baseNumber)


def createCSVBigNames(person: str, i: int):
    csv2create = []
    csv2create.append([f"{person.capitalize()} OKR's", ])
    rawData = pd.read_csv("rawData.csv")
    responsabilities = personResponsabilitiesBigNames(person)
    paises = responsabilities['paises']
    divisiones = responsabilities['divisiones']
    columnas = ['Metric']
    for pais in paises:
        columnas = columnas + miniColumnaPerCountry(pais)
    csv2create.append(columnas)
    for organizationName, listOfRows in divisiones.items():
        csv2create.append([organizationName,])
        for row in listOfRows:
            list2append = [row,]
            for columna in columnas[1:]:
                list2append.append(
                    makePrettyBaseNumber(rawData[rawData['Requirements'] == row][columna].values[0]))
            csv2create.append(list2append)
    createCSVbyList(csv2create, f'{i}{person}OKRs.csv')


def main():
    bigNames = ['catalinaarteaga', 'patriciacatalunadiaz',
                'tomasjaramillo', 'sergiocanal']
    for i, name in enumerate(bigNames):
        createCSVBigNames(name, i)

main()
