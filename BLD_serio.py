import csv
import os
import pandas as pd
from pprint import pprint
from BD_data import BD, BD_ML, getBDLs, structureForDistribution
from OKRsData import plus5OrdersRegion, newAdquireRsRegion, ordersOfNewAdquireRsRegion, generalDailyOrdersRegion


def createFolderIfNotExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def isBoth(column):
    if column in ['SME Total Rs Acquired (By BDs)', 'CKA Total Rs Acquired (By BDs)']:
        return False
    return True


def getColumnsByRoleOrganization(role, organization):
    FarmingCKAData = ['Daily Orders CKA', 'Daily Orders of CKA Rs acquired in 2024',
                      'CKA # of R1s  (5+ Daily Orders)', 'Promotional Coverage', 'Promotion quality', 'CKAs B cancellation rate', 'CKAs imperfect orders',]
    FarmingSMEData = ['Daily Orders SME',
                      'SME Daily Orders for Rs FO in current year', 'SME # of R1s  (5+ Daily Orders)', 'Promotional Coverage', 'Promotion quality',]
    HuntingCKAData = ['Daily Orders CKA',
                      'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024', 'CKA # of R1s  (5+ Daily Orders)']
    HuntingSMEData = ['Daily Orders SME', 'SME Daily Orders for Rs FO in current year',
                      'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)']
    if role == 'Farming' or role == 'Farmer':
        if organization == 'CKA':
            return FarmingCKAData
        return FarmingSMEData
    else:
        if organization == 'CKA':
            return HuntingCKAData
        return HuntingSMEData


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


def prettifyName(name):
    name = name.replace('á', 'a').replace('é', 'e').replace(
        'í', 'i').replace('ó', 'o').replace('ú', 'u')
    if name == 'Bogota, D.C.':
        return 'Bogota D.C.'
    if name == 'Juarez(CHIH)':
        return 'Juarez CHIH'
    return name


def countryOfRegion(region):
    if region in ['Norte', 'CDMX', 'Pacifico', 'Sur']:
        return 'MX'
    if region in ['San Jose']:
        return 'CR'
    if region in ['Lima']:
        return 'PE'
    return 'CO'


def getInterestingDataPerStructure(structure: dict, roleParameter: str, organizationParameter: str):
    interesting = {}
    for region, dict in structure.items():
        for organization, miniDict in dict.items():
            for role, cantity in miniDict.items():
                if role == roleParameter and organization == organizationParameter:
                    key = f'{region}_{organization}_{role}'
                    interesting[key] = cantity
    return interesting


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


def makePrettyBaseNumber(baseNumber):
    if 'k' in baseNumber:
        return float(baseNumber.replace('k', '')) * 1000
    elif baseNumber == 'TBD':
        return 'TBD'
    return float(baseNumber)


def main():
    bdls = getBDLs()
    rawData = pd.read_csv('rawData.csv')
    result = {}
    # for bdl in bdls:
    #     pprint(bdl.structureForBDL())
    #     print()
    # print()
    # print()
    # bdsStructure = structureForDistribution()
    # pprint(bdsStructure)
    # return

    for bdl in bdls:
        structure = bdl.structureForBDL()
        dataDenominadores = structureForDistribution()
        combinaciones = bdl.combinaciones4columns()
        dataImportante: dict = {}

        for combinacion in combinaciones:
            role, organization = combinacion.split('_')
            columns = getColumnsByRoleOrganization(
                role, organization)
            allInterestingData = getInterestingDataPerStructure(
                structure, role, organization)
            for column in columns:
                if column not in dataImportante:
                    dataImportante[column] = {}
                table = getTablePerColumn(column)
                if column in ['Promotional Coverage', 'Promotion quality', 'CKAs B cancellation rate', 'CKAs imperfect orders']:
                    miniColumns = miniColumnaPerCountry(
                        'NOIMPORTA', all=True)
                    for miniColumn in miniColumns:
                        if miniColumn not in dataImportante[column]:
                            dataImportante[column][miniColumn] = 0
                        try:
                            datoBase = rawData[rawData['Requirements']
                                               == column][miniColumn].values[0]
                        except:
                            if 'Baseline' in miniColumn:
                                datoBase = rawData[rawData['Requirements']
                                                   == column]['MX - Baseline'].values[0]
                            else:
                                datoBase = rawData[rawData['Requirements']
                                                   == column]['MX - Target'].values[0]

                        dataImportante[column][miniColumn] = datoBase
                    continue
                for dataInteresante in allInterestingData:
                    regionIntersante, organizationIntersante, roleIntersante = dataInteresante.split(
                        '_')
                    countryInteresante = countryOfRegion(regionIntersante)
                    miniColumns = miniColumnaPerCountry(
                        countryInteresante, regionIntersante)
                    names2save = None
                    if len(miniColumns) > 2:
                        names2save = miniColumns[:2]
                        miniColumns = (miniColumns[2], miniColumns[3])
                    for i, miniColumn in enumerate(miniColumns):
                        if names2save == None:
                            if miniColumn not in dataImportante[column]:
                                dataImportante[column][miniColumn] = 0
                        else:
                            if names2save[i] not in dataImportante[column]:
                                dataImportante[column][names2save[i]] = 0

                        intermidiumState = rawData[rawData['Requirements']
                                                   == column][miniColumn]
                        if intermidiumState.empty:
                            print(f'No se encontro tabla para {column}')
                            raise ValueError
                        baseNumber = intermidiumState.values[0]
                        baseNumber = makePrettyBaseNumber(baseNumber)
                        if baseNumber == 'TBD':
                            if names2save == None:
                                dataImportante[column][miniColumn] = 'TBD'
                                continue
                            else:
                                dataImportante[column][names2save[i]] = 'TBD'
                                continue
                        porcentajePerRegion = table[organizationIntersante][countryInteresante][regionIntersante]
                        porcentajeAporte = 0
                        if isBoth(column):
                            numerador = structure[regionIntersante][organizationIntersante][roleIntersante]
                            denominador = dataDenominadores[regionIntersante][
                                organizationIntersante]['Both']
                        else:
                            numerador = structure[regionIntersante][organizationIntersante][roleIntersante]
                            denominador = dataDenominadores[regionIntersante][
                                organizationIntersante][roleIntersante]
                        porcentajeAporte = (numerador / denominador)
                        if names2save == None:
                            dataImportante[column][miniColumn] += porcentajePerRegion * \
                                porcentajeAporte * baseNumber
                        else:
                            dataImportante[column][names2save[i]] += porcentajePerRegion * \
                                porcentajeAporte * baseNumber
        for column, miniDict in dataImportante.items():
            for miniColumn, value in miniDict.items():
                if value != 'TBD':
                    if not isBoth(column):
                        # dataImportante[column][miniColumn] = value/2
                        pass
                    # dataImportante[column][miniColumn] = round(value)
        result[bdl.name] = dataImportante
    # pprint(result)
    return result


def itsWorking(data, columnParameter):
    lalis = {}
    for bdName, dictWithStuff in data.items():
        for column, miniDict in dictWithStuff.items():
            if column == columnParameter:
                for miniColumn, value in miniDict.items():
                    if miniColumn not in lalis:
                        lalis[miniColumn] = 0
                    try:
                        if value != 'TBD' and not ('%' in str(value)):
                            lalis[miniColumn] += value
                        else:
                            lalis[miniColumn] = value
                    except:
                        print(bdName, column, miniColumn, value)
                        raise ValueError
    pprint(lalis)
    rawData = pd.read_csv('rawData.csv')
    print(rawData[rawData['Requirements'] == columnParameter].values[0][1:])


def check(data):
    rawData = pd.read_csv('rawData.csv')
    columns = rawData['Requirements'].unique()
    for column in columns:
        print(column)
        itsWorking(data, column)
        print()
        print()


def keepImportantStuff(bds_data):
    stuff = {}
    for bd, data in bds_data.items():
        dataRelevant2Keep = []
        for column, miniDict in data.items():
            if column not in ['Promotional Coverage', 'Promotion quality', 'CKAs B cancellation rate', 'CKAs imperfect orders']:
                for miniColumn, value in miniDict.items():
                    if miniColumn not in dataRelevant2Keep:
                        dataRelevant2Keep.append(miniColumn)
        stuff[bd] = dataRelevant2Keep
    # lets delete all miniColumns that are not in dataRelevant2Keep
    for bd, data in bds_data.items():
        dataRelevant2Keep = stuff[bd]
        for column, miniDict in data.items():
            for miniColumn in list(miniDict.keys()):
                if miniColumn not in dataRelevant2Keep:
                    del bds_data[bd][column][miniColumn]
    for bd, data in bds_data.items():
        for column, miniDict in data.items():
            for importante in stuff[bd]:
                if importante not in miniDict:
                    bds_data[bd][column][importante] = 0
    return bds_data, stuff


def csv4bd(bds_data, columnsPerBd):
    createFolderIfNotExists('BDL_tables')
    for bd, data in bds_data.items():
        filename = f"BDL_tables/{bd}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            header = ['Metric'] + columnsPerBd[bd]
            writer.writerow(header)
            # Write data
            for metric, values in data.items():
                row = [metric]
                for column in columnsPerBd[bd]:
                    value = values.get(column, 0)
                    if value == 'TBD' or ('%' in str(value)):
                        row.append(value)
                    else:
                        row.append(round(float(value)))
                writer.writerow(row)
    print("CSV files created successfully.")


print("CSV files created successfully.")


if __name__ == '__main__':
    data = main()
    # check(data)
    data, stuff = keepImportantStuff(data)
    csv4bd(data, stuff)
