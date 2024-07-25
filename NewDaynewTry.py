import csv
import os
from pprint import pprint
import pandas as pd
from OKRsData import plus5OrdersRegion, newAdquireRsRegion, ordersOfNewAdquireRsRegion, generalDailyOrdersRegion


def getColumns(ForH='Both', organization='Both', name=None):
    allCKA = ['Daily Orders CKA', 'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024', 'CKA # of R1s  (5+ Daily Orders)', 'CKAs B cancellation rate', 'CKAs imperfect orders',
              'CKA Meal Loss % GMV', 'CKA B App orders on time rate', 'CKA # Orders CDMX',  'CKA # Orders MTY', 'CKA # Orders GDL', 'CKA # Orders BOG', 'CKA # Orders MED', 'Promotional Coverage', 'Promotion quality']

    allSME = ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
              'SME Meal Loss % GMV', 'SME B App orders on time rate', 'SME # Orders CDMX', 'SME # Orders MTY', 'SME # Orders GDL', 'SME # Orders BOG', 'SME # Orders MED', 'Promotional Coverage', 'Promotion quality']

    exclusions = ['Promotional Coverage', 'Promotion quality']

    # Filter out elements from allCKA and allSME lists based on exclusions
    allCKA = [item for item in allCKA if item not in exclusions]
    allSME = [item for item in allSME if item not in exclusions]

    if name == 'patri' or name == 'grace':
        exclusions = ['CKA # Orders CDMX',  'CKA # Orders MTY', 'CKA # Orders GDL',
                      'SME # Orders CDMX', 'SME # Orders MTY', 'SME # Orders GDL']
        allCKA = [item for item in allCKA if item not in exclusions]
        allSME = [item for item in allSME if item not in exclusions]

    if name == 'tomi':
        exclusions = ['CKA # Orders BOG',  'CKA # Orders MED',
                      'SME # Orders BOG', 'SME # Orders MED']
        allCKA = [item for item in allCKA if item not in exclusions]
        allSME = [item for item in allSME if item not in exclusions]

    if ForH == 'Both' and organization == 'Both':
        return allCKA, allSME
    if organization == 'CKA':
        if ForH == 'Both':
            return allCKA
        if ForH == 'Hunting' or ForH == 'Hunter' or ForH == 'H':
            return ['Daily Orders CKA', "CKA Total Rs Acquired (By BDs)", "Daily Orders of CKA Rs acquired in 2024",]
    else:
        if ForH == 'Both':
            return allSME


def getNiceName(name: str) -> str:
    name_dict = {
        'catalinaarteaga': 'Catalina Arteaga',
        'patriciacatalunadiaz': 'Patricia Cataluna Diaz',
        'tomasjaramillo': 'Tomas Jaramillo',
        'sergiocanal': 'Sergio Canal',
        'juanpablonostitajer': 'Juan Pablo Nostita Jer',
        'alejandroLelo': 'Alejandro Lelo',
        'gracielarios': 'Graciela Rios',
        'jaimefuster': 'Jaime Fuster',
        'erikafragosovega': 'Erika Fragoso Vega',
        'grenteriavillasuso': 'Grenteria Villasuso',
        'NoNameYet': 'No Name Yet'
    }
    if name in name_dict:
        return name_dict[name]
    return name


def miniColumnaPerCountry(country, region=None, all=False):
    if all:
        return ['CO  - Baseline', 'CO  - Target', 'MX - Baseline', 'MX - Target', 'CR  - Baseline', 'CR  - Target', 'PE  - Baseline', 'PE  - Target', 'Norte - Baseline', 'Norte - Target', 'CDMX - Baseline', 'CDMX - Target', 'Pacifico - Baseline', 'Pacifico - Target', 'Sur - Baseline', 'Sur - Target']
    if country == 'CO':
        if region != None:
            return [f'{region} - Baseline', f'{region} - Target', 'CO  - Baseline', 'CO  - Target']
        else:
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


def isPais(paisRegion: str):
    if paisRegion in ('CO', 'MX', 'CR', 'PE'):
        return True
    else:
        return False


def paisDeRegion(region: str):
    if region in ['Norte', 'Sur', 'Pacifico', 'CDMX']:
        return 'MX'
    else:
        return 'CO'


def personResponsabilitiesBigNames(person: str):
    data = {
        'catalinaarteaga': {
            'paises': ['MX', 'CO', 'PE', 'CR',],
            'divisiones': {'CKA': getColumns(organization='CKA'),
                           'SME': getColumns(organization='SME')}
        },
        'patriciacatalunadiaz': {
            'paises': ['CO', 'PE', 'CR',],
            'divisiones': {'CKA': getColumns(organization='CKA', name='patri'),
                           'SME': getColumns(organization='SME', name='patri')}
        },
        'tomasjaramillo': {
            'paises': ['MX',],
            'divisiones': {'SME': getColumns(organization='SME', name='tomi')}
        },
        'sergiocanal': {
            'paises': ['MX',],
            'divisiones': {'CKA': ['Daily Orders CKA', 'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024', 'CKA # Orders CDMX',  'CKA # Orders MTY', 'CKA # Orders GDL',], }
        },
        'juanpablonostitajer': {
            'paises': ['CDMX',],
            'divisiones': {'CKA': getColumns('Hunter', 'CKA'), }
        },
        'alejandroLelo': {
            'paises': ['Norte', 'Sur', 'Pacifico',],
            'divisiones': {'CKA': getColumns('Hunter', 'CKA'), }
        },
        'gracielarios': {
            'paises': ['CO', 'PE', 'CR',],
            'divisiones': {'CKA': getColumns(organization='CKA', name='grace'), }
        },
        'jaimefuster': {
            'paises': ['Norte'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
        'erikafragosovega': {
            'paises': ['CDMX'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
        'grenteriavillasuso': {
            'paises': ['Pacifico'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
        'NoNameYet': {
            'paises': ['CO', 'PE', 'CR'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
    }
    if person in data:
        return data[person]
    else:
        print('la persona que buscas no existe en esta seccion')
        print(person)

        raise ValueError


def getTablePerColumn(column: str):
    plus5Columns: set = {
        'SME # of R1s  (5+ Daily Orders)', 'CKA # of R1s  (5+ Daily Orders)', 'SME # of R1s  (5+ Daily Orders)', 'CKA  # of R1s  (5+ Daily Orders)'}
    newAdquireColumns: set = {
        'CKA Total Rs Acquired (By BDs)',  'SME Total Rs Acquired (By BDs)'}
    ordersOfNewAdquireColumns: set = {
        'SME Daily Orders for Rs FO in current year', 'SME Daily Orders for Rs FO in current year', 'Daily Orders of CKA Rs acquired in 2024', 'Daily Orders of CKA Rs acquired in 2024'}
    generalDailyOrdersColumns: set = {'Daily Orders CKA', 'Daily Orders SME'}
    if column in plus5Columns:
        return plus5OrdersRegion
    if column in newAdquireColumns:
        return newAdquireRsRegion
    if column in ordersOfNewAdquireColumns:
        return ordersOfNewAdquireRsRegion
    if column in generalDailyOrdersColumns:
        return generalDailyOrdersRegion
    return None


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
    csv2create.append([f"{getNiceName(person)} OKR's", ])
    rawData = pd.read_csv("rawData.csv")
    responsabilities = personResponsabilitiesBigNames(person)
    paises = responsabilities['paises']
    divisiones = responsabilities['divisiones']
    columnas = ['Metric']
    evaluationCountries = True if isPais(paises[0]) else False
    traductorColumnaRealFake = None
    if not evaluationCountries:
        traductorColumnaRealFake = {}

    for paisOrRegion in paises:
        if evaluationCountries:
            columnas = columnas + miniColumnaPerCountry(paisOrRegion)
        else:
            pais = paisDeRegion(paisOrRegion)
            temporal = miniColumnaPerCountry(pais, paisOrRegion)
            reales = [temporal[2], temporal[3]]
            postizas = temporal[:2]
            traductorColumnaRealFake[postizas[0]] = reales[0]
            traductorColumnaRealFake[postizas[1]] = reales[1]
            columnas = columnas + postizas

    csv2create.append(columnas)
    for organizationName, listOfRows in divisiones.items():
        csv2create.append([organizationName,])
        for row in listOfRows:
            list2append = [row,]
            tabla = None
            if not evaluationCountries:
                tabla = getTablePerColumn(row)
            for index, columna in enumerate(columnas[1:]):
                if evaluationCountries:
                    list2append.append(
                        makePrettyBaseNumber(rawData[rawData['Requirements'] == row][columna].values[0]))
                else:
                    realColumna = traductorColumnaRealFake[columna]

                    if tabla == None:
                        list2append.append(
                            makePrettyBaseNumber(rawData[rawData['Requirements'] == row][realColumna].values[0]))

                    else:
                        region = columna.split('-')[0].strip()
                        pais = paisDeRegion(region)
                        multiplicador = tabla[organizationName][pais][region]
                        list2append.append(
                            round(multiplicador*(makePrettyBaseNumber(rawData[rawData['Requirements'] == row][realColumna].values[0]))))

            csv2create.append(list2append)

    createCSVbyList(csv2create, f'{chr(i+97)}_{getNiceName(person)}OKRs.csv')


def main():
    bigNames = ['catalinaarteaga', 'patriciacatalunadiaz', 'tomasjaramillo', 'sergiocanal', 'juanpablonostitajer',
                'alejandroLelo', 'gracielarios', 'jaimefuster', 'erikafragosovega', 'grenteriavillasuso', 'NoNameYet']

    for i, name in enumerate(bigNames):
        createCSVBigNames(name, i)


main()
