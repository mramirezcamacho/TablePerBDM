import csv
import os
from pprint import pprint
import pandas as pd
from OKRsData import plus5OrdersRegion, newAdquireRsRegion, ordersOfNewAdquireRsRegion, generalDailyOrdersRegion, generatePerRegionPersonalizado


def meIncumbe(bd_type: str, OKR: str):
    if bd_type == 'Hibrido':
        return True
    if 'Daily Orders' in OKR and '5+' not in OKR:
        return True
    if 'Total Rs Acquired (By BDs)' in OKR:
        if bd_type == 'Hunting':
            return True
        else:
            return False
    if bd_type == 'Farming':
        return True
    else:
        return False


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

    if name == 'gabrielrenowitzky':
        allCKA = ['CKAs B cancellation rate', 'CKAs imperfect orders',
                  'CKA Meal Loss % GMV', 'CKA B App orders on time rate',]
        allSME = ['SME B cancel % orders', 'SME imperfect orders',
                  'SME Meal Loss % GMV', 'SME B App orders on time rate',]

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
        'grenteriavillasuso': 'Guillermo Renteria',
        'MAC BDL': 'MAC BDL',
        'juanvargas': 'Juan Vargas',
        'gabrielrenowitzky': 'Gabriel Renowitzky',
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
            'paises': ['MX',],
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
        'juanvargas': {
            'paises': ['Sur'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
        'MAC BDL': {
            'paises': ['CO', 'PE', 'CR'],
            'divisiones': {'SME': ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year', 'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)', 'SME B cancel % orders', 'SME imperfect orders',
                                   'SME Meal Loss % GMV', 'SME B App orders on time rate'], }
        },
        'gabrielrenowitzky': {
            'paises': ['MX', 'CO', 'PE', 'CR'],
            'divisiones': {'SME': getColumns(organization='SME', name='gabrielrenowitzky'),
                           'CKA': getColumns(organization='CKA', name='gabrielrenowitzky')}
        }}
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
        return round(float(baseNumber.replace('k', '')) * 1000)
    elif baseNumber == 'TBD':
        return 'TBD'
    elif '%' in baseNumber:
        return baseNumber
    return round(float(baseNumber))


def fileAndColumnFilePerColumn(column: str):
    plus5Columns: set = {
        'SME # of R1s  (5+ Daily Orders)', 'CKA # of R1s  (5+ Daily Orders)', 'SME # of R1s  (5+ Daily Orders)', 'CKA  # of R1s  (5+ Daily Orders)'}
    newAdquireColumns: set = {
        'CKA Total Rs Acquired (By BDs)',  'SME Total Rs Acquired (By BDs)'}
    ordersOfNewAdquireColumns: set = {
        'SME Daily Orders for Rs FO in current year', 'SME Daily Orders for Rs FO in current year', 'Daily Orders of CKA Rs acquired in 2024', 'Daily Orders of CKA Rs acquired in 2024'}
    generalDailyOrdersColumns: set = {'Daily Orders CKA', 'Daily Orders SME'}
    if column in plus5Columns:
        return ('plus5orderRs.csv', '5 + order store count(week total)')
    if column in newAdquireColumns:
        return ('newRsOrders.csv', 'shop_cnt')
    if column in ordersOfNewAdquireColumns:
        return ('newRsOrders.csv', 'complete_orders')
    if column in generalDailyOrdersColumns:
        return ('generalDailyOrders.csv', 'Daily Orders')


def createCSVBigNames(person: str, i: int):
    csv2create = []
    forLater = dict()
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
        list2append = [organizationName,]
        while len(list2append) < len(columnas):
            list2append.append('-')
        csv2create.append(list2append)
        for row in listOfRows:
            list2append = [row,]
            tabla = None
            if not evaluationCountries:
                tabla = getTablePerColumn(row)
            for index, columna in enumerate(columnas[1:]):
                if evaluationCountries:
                    list2append.append(
                        makePrettyBaseNumber(rawData[rawData['Requirements'] == row][columna].values[0]))
                    if row not in forLater:
                        forLater[row] = {}
                    if 'Target' in columna:
                        countryOrRegion = columna.split('-')[0].strip()
                        forLater[row][countryOrRegion] = makePrettyBaseNumber(
                            rawData[rawData['Requirements'] == row][columna].values[0])
                else:
                    realColumna = traductorColumnaRealFake[columna]

                    if tabla == None:
                        list2append.append(
                            makePrettyBaseNumber(rawData[rawData['Requirements'] == row][realColumna].values[0]))
                        if row not in forLater:
                            forLater[row] = {}
                        if 'Target' in columna:
                            countryOrRegion = columna.split('-')[0].strip()
                            forLater[row][countryOrRegion] = makePrettyBaseNumber(
                                rawData[rawData['Requirements'] == row][realColumna].values[0])
                    else:
                        region = columna.split('-')[0].strip()
                        pais = paisDeRegion(region)
                        multiplicador = tabla[organizationName][pais][region]
                        list2append.append(
                            round(multiplicador*(makePrettyBaseNumber(rawData[rawData['Requirements'] == row][realColumna].values[0]))))
                        if row not in forLater:
                            forLater[row] = {}
                        if 'Target' in columna:
                            forLater[row][region] = round(multiplicador*(makePrettyBaseNumber(
                                rawData[rawData['Requirements'] == row][realColumna].values[0])))

            csv2create.append(list2append)
    if person in getInferiores():
        csv2create.append([])
        csv2create.append([])
        columnas = ['BDM',]
        for organizationName, listOfRows in divisiones.items():
            for row in listOfRows:
                if '# Orders' not in row:
                    columnas.append(row)
        csv2create.append(columnas)
        inferiores = getInferiores()[person]
        aporteBDsPerDivisiones = None
        for bd_name, description in inferiores.items():
            if 'numberOfBDs' in description:
                aporteBDsPerDivisiones = {}
        if aporteBDsPerDivisiones != None:
            for organizationName, listOfColumns in divisiones.items():
                if organizationName not in aporteBDsPerDivisiones:
                    aporteBDsPerDivisiones[organizationName] = {}
                for column in listOfColumns:
                    if column not in aporteBDsPerDivisiones:
                        aporteBDsPerDivisiones[organizationName][column] = 0
                    for BDM_name, description in inferiores.items():
                        if meIncumbe(description['type'], column):
                            aporteBDsPerDivisiones[organizationName][column] += description['numberOfBDs']

        for bd_name, description in inferiores.items():
            try:
                typeBD, regionBD, verticalBD, countryBD = description['type'], description[
                    'region'], description['vertical'], description['country']
            except:
                typeBD, verticalBD, numberOfBDs, countryBD = description[
                    'type'], description['vertical'], description['numberOfBDs'], description['country']
            typeBonito = 'Hunter' if typeBD == 'Hunting' else 'Farmer'
            list2append = [bd_name+f' OKRs ({typeBonito})',]
            for organizationName, listOfColumns in divisiones.items():
                for column in listOfColumns:
                    if '# Orders' not in column:
                        if meIncumbe(typeBD, column):
                            baseNumber = forLater[column][countryBD]
                            try:
                                fileName, columnName = fileAndColumnFilePerColumn(
                                    column)
                            except:
                                list2append.append(forLater[column][countryBD])
                                continue
                            if aporteBDsPerDivisiones != None:
                                list2append.append(
                                    round(baseNumber*(numberOfBDs/aporteBDsPerDivisiones[verticalBD][column])))
                            else:
                                if 'All' in regionBD:
                                    multiplier = generatePerRegionPersonalizado(
                                        fileName, columnName, countryParameter=countryBD, vertical=verticalBD, excluding=['Nadita nada'])
                                    list2append.append(
                                        round(baseNumber*multiplier))
                                elif 'excluding' in description:
                                    multiplier = generatePerRegionPersonalizado(
                                        fileName, columnName, countryParameter=countryBD, vertical=verticalBD, excluding=description['excluding'])
                                    list2append.append(
                                        round(baseNumber*multiplier))
                                else:
                                    multiplier = generatePerRegionPersonalizado(
                                        fileName, columnName, countryParameter=countryBD, vertical=verticalBD, regions=regionBD)
                                    list2append.append(
                                        round(baseNumber*multiplier))
                        else:
                            list2append.append('N/A')
            csv2create.append(list2append)

    createCSVbyList(csv2create, f'{chr(i+97)}_{getNiceName(person)}OKRs.csv')


def getInferiores():
    inferiores = {
        'gracielarios': {
            "Juan Gomez": {"type": "Hibrido", "region": "Bogota D.C.", "vertical": "CKA", 'country': 'CO'},
            "Marcela Castano": {"type": "Hibrido", "region": "Medellin", "vertical": "CKA", 'country': 'CO'},
            "Marco Rojas": {"type": "Hibrido", "region": "All Peru", "vertical": "CKA", 'country': 'PE'},
            "Kevin Molina": {"type": "Hibrido", "region": "All Costa Rica", "vertical": "CKA", 'country': 'CR'},
            "Daniela Ramirez": {"type": "Hibrido", "region": "Rest CO", "vertical": "CKA", 'country': 'CO', 'excluding': ['Bogota D.C.', 'Medellin']},
        },
        'juanvargas': {
            "Amauri Martinez": {"type": "Hunting", "vertical": "SME", 'numberOfBDs': 11, 'country': 'Sur'},
            "Carlos Lozano": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Sur'},
            "Cindy Ibarra": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Sur'},
            "Jose Pablo Maldonado": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 8, 'country': 'Sur'},
            "Miguel Angel Kirvan": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Sur'},
        },
        'erikafragosovega': {
            "Jorge Garcia": {"type": "Hunting", "vertical": "SME", 'numberOfBDs': 6, 'country': 'CDMX'},
            "Jorge Renato Sotelo": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'CDMX'},
            "Juan Jose Fierro": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 8, 'country': 'CDMX'},
            "Karin Luna": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 9, 'country': 'CDMX'},
            "Luis Enrique Quintero": {"type": "Hunting", "vertical": "SME", 'numberOfBDs': 6, 'country': 'CDMX'},
            "Riccardo Picone": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 8, 'country': 'CDMX'},
        },
        'grenteriavillasuso': {
            "Antonio Topete": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Pacifico'},
            "Bertin Mendoza": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 6, 'country': 'Pacifico'},
            "David Rabago": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Pacifico'},
            "Edgar Hazel Cisneros": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Pacifico'},
            "Emmanuel Ochoa Quintero": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 10, 'country': 'Pacifico'},
            "Luis Angel Ballesteros": {"type": "Hunting", "vertical": "SME", 'numberOfBDs': 5, 'country': 'Pacifico'},
            "Luis Fernando Gutierrez": {"type": "Farming", "vertical": "SME", 'numberOfBDs': 8, 'country': 'Pacifico'},
            "Sandra Martinez": {"type": "Hunting", "vertical": "SME", 'numberOfBDs': 6, 'country': 'Pacifico'},
        },
        'jaimefuster': {
            "Christian Enrique": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 6, 'country': 'Norte'},
            "Cristopher Chocoteco": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 7, 'country': 'Norte'},
            "Cynthia Judith Espinosa": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 8, 'country': 'Norte'},
            "Fernando Javier": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 5, 'country': 'Norte'},
            "Francisco Armando": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 9, 'country': 'Norte'},
            "Juan Arturo Estrada": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 9, 'country': 'Norte'},
            "Manuel San Juan": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 4, 'country': 'Norte'},
            "Juan Eduardo Soto": {"type": "Hibrido", "vertical": "SME", 'numberOfBDs': 8, 'country': 'Norte'},
        },
        'MAC BDL': {
            "Daniel Montalvo": {"type": "Farming", "region": "Bogota D.C. + Ciudades", "vertical": "SME", 'country': 'CO', 'excluding': ['Cali', 'Medellin']},
            "Jackeline": {"type": "Farming", "region": "Medellin", "vertical": "SME", 'country': 'CO'},
            "Federico Sonallia": {"type": "Farming", "region": "Cali", "vertical": "SME", 'country': 'CO'},
            "Omar Amayo": {"type": "Hibrido", "region": "All Peru", "vertical": "SME", 'country': 'PE'},
            "Mauricio Montero": {"type": "Hibrido", "region": "All Costa Rica", "vertical": "SME", 'country': 'CR'},
            "Julian Serrano": {"type": "Hunting", "region": "All Colombia", "vertical": "SME", 'country': 'CO'}
        }
    }
    return inferiores


def main():
    bigNames = ['catalinaarteaga', 'patriciacatalunadiaz', 'tomasjaramillo', 'sergiocanal', 'juanpablonostitajer',
                'alejandroLelo', 'gracielarios', 'jaimefuster', 'erikafragosovega', 'juanvargas', 'grenteriavillasuso', 'MAC BDL', 'gabrielrenowitzky']

    for i, name in enumerate(bigNames):
        createCSVBigNames(name, i)


main()
