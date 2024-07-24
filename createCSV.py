import csv
import os
from pprint import pprint
import pandas as pd
from BD_data import BD, BD_ML, citiesPerBDM, distributionOfBDsPerCountryPerRolePerOrganization
from OKRsData import plus5Orders, newAdquireRs, ordersOfNewAdquireRs, generalDailyOrders


def createFolderIfNotExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def getCSVDistribution():
    FarmingCKAData = ['Daily Orders CKA', 'CKA Daily Orders for Rs FO in current year',
                      'CKA # of R1s  (5+ Daily Orders)', 'Promotional Coverage', 'Promotion quality', 'CKAs B cancellation rate', 'CKAs imperfect orders',]
    FarmingSMEData = ['Daily Orders SME',
                      'SME Daily Orders for Rs FO in current year', 'SME # of R1s  (5+ Daily Orders)', 'Promotional Coverage', 'Promotion quality',]
    HuntingCKAData = ['Daily Orders CKA',
                      'CKA Total Rs Acquired (By BDs)', 'Daily Orders of CKA Rs acquired in 2024', 'CKA # of R1s  (5+ Daily Orders)']
    HuntingSMEData = ['Daily Orders SME', 'Daily Orders of Rs acquired in 2024',
                      'SME Total Rs Acquired (By BDs)', 'SME # of R1s  (5+ Daily Orders)']
    returnData = {'FCKA': FarmingCKAData, 'FSME': FarmingSMEData,
                  'HCKA': HuntingCKAData, 'HSME': HuntingSMEData}
    return returnData


def createTxtExplaining(bd, FarmingHunting, CKASME, pais):
    createFolderIfNotExists(f'results/{bd.bd_type}/{bd.name}')
    with open(f'results/{bd.bd_type}/{bd.name}/{bd.name}_{FarmingHunting}_{CKASME}_{pais}_{bd.bd_type}.txt', 'w') as file:
        file.write(f'{FarmingHunting} {bd.bd_type} {bd.name}\n')
        file.write(f'{CKASME}\n')
        file.write('Tiene los siguientes BDs:\n')
        roleBD = ''
        if FarmingHunting == 'Farming':
            roleBD = 'Farmer'
        else:
            roleBD = 'Hunter'
        for miniBd in bd.bds:
            if miniBd.role == roleBD and miniBd.RsType == CKASME:
                file.write(f'{str(miniBd)}\n')


def getTablePerColumn(column: str):
    plus5Columns: set = {
        'SME # of R1s  (5+ Daily Orders)', 'CKA # of R1s  (5+ Daily Orders)', 'SME # of R1s  (5+ Daily Orders)', 'CKA  # of R1s  (5+ Daily Orders)'}
    newAdquireColumns: set = {
        'CKA Total Rs Acquired (By BDs)',  'SME Total Rs Acquired (By BDs)'}
    ordersOfNewAdquireColumns: set = {
        'Daily Orders of Rs acquired in 2024', 'SME Daily Orders for Rs FO in current year', 'CKA Daily Orders for Rs FO in current year', 'Daily Orders of CKA Rs acquired in 2024'}
    generalDailyOrdersColumns: set = {'Daily Orders CKA', 'Daily Orders SME'}
    if column in plus5Columns:
        return plus5Orders
    if column in newAdquireColumns:
        return newAdquireRs
    if column in ordersOfNewAdquireColumns:
        return ordersOfNewAdquireRs
    if column in generalDailyOrdersColumns:
        return generalDailyOrders
    return None


def createCSV(data, FarmingHunting, CKASME, pais, bd):
    createFolderIfNotExists(f'results/{bd.bd_type}/{bd.name}')
    csv_file_path = f'baseCSV/{FarmingHunting} BDMs {CKASME}.csv'
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    for i, row in enumerate(rows):
        for j, column in enumerate(row):
            if '[' in column:
                rows[i][j] = column.replace('[', '').replace(']', '')
                rows[i][j] = data[int(rows[i][j])]

    # Write the modified content back to the CSV file
    csv_final_file_path = f'results/{bd.bd_type}/{bd.name}/{bd.name}_{FarmingHunting}_{CKASME}_{pais}_{bd.bd_type}.csv'
    with open(csv_final_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def getRawData():
    data = pd.read_csv('rawData.csv')
    return data


def pair(bdML: BD_ML):
    FH_data = getCSVDistribution()


def main():
    bds = citiesPerBDM()
    # for x in bds:
    #     print(x.name)
    #     print()
    #     pprint(x.calculateDistribution())
    #     print()
    #     pprint(x.organizarDistribution())
    #     print()
    #     pprint(x.paises4role())
    #     print()
    #     pprint(x.calculateDistribution4search())
    #     return
    columnsNeeded = getCSVDistribution()
    rawData = getRawData()
    for bd in bds:
        secciones = list(bd.organizarDistribution().keys())
        for seccion in secciones:
            data = []
            data.append(bd.name)
            # print(seccion)
            # pprint(paises4rol)
            # return
            ForH = seccion[0]
            role = ''
            if ForH == 'F':
                role = 'Farmer'
            else:
                role = 'Hunter'
            organization = seccion[1:]
            keys = []
            for key in list(bd.calculateDistribution().keys()):
                if role in key and organization in key:
                    keys.append(key)
            valuesToConsider = {}
            for key in keys:
                valuesToConsider[key] = bd.calculateDistribution(
                )[key]/distributionOfBDsPerCountryPerRolePerOrganization()[key]
            paises2consider: list = []
            for key in list(valuesToConsider.keys()):
                if key.split('_')[1] not in paises2consider:
                    paises2consider.append(key.split('_')[1])
            paises2consider.sort()

            columns = columnsNeeded[seccion]
            for column in columns:
                table = getTablePerColumn(column)
                numbers = rawData[rawData['Requirements'] == column].copy()
                for i, miniColumna in enumerate(numbers.columns[1:]):
                    if column == 'Promotional Coverage' or column == 'Promotion quality':
                        data.append('TBD')
                        continue
                    if column == 'CKAs B cancellation rate' or column == 'CKAs imperfect orders':
                        for paises in paises2consider:
                            if paises not in miniColumna:
                                data.append('0')
                            else:
                                toAppend = list(
                                    rawData[rawData['Requirements'] == column].values[0][1:])
                                data.append(toAppend[i])
                        continue

                    suma = 0
                    number = numbers[miniColumna].values[0]
                    percentage = False
                    if '%' in number:
                        number = number.replace('%', '')
                        number = float(number)/100
                        number = str(number)
                        percentage = True
                    if number == 'TBD':
                        data.append('TBD')
                        continue
                    if 'k' in number:
                        number = number.replace('k', '')
                        number = float(number)*1000
                    else:
                        number = float(number)
                    for pais in paises2consider:
                        if pais in miniColumna:
                            for key, value in valuesToConsider.items():
                                if pais in key:
                                    ciudad = key.split('_')[2]
                                    if "Bogot" in ciudad:
                                        ciudad = 'Bogotá D.C.'
                                    if 'á' in ciudad:
                                        ciudad = ciudad.replace('á', 'a')
                                    if 'é' in ciudad:
                                        ciudad = ciudad.replace('é', 'e')
                                    if 'í' in ciudad:
                                        ciudad = ciudad.replace('í', 'i')
                                    if 'ó' in ciudad:
                                        ciudad = ciudad.replace('ó', 'o')
                                    if 'ú' in ciudad:
                                        ciudad = ciudad.replace('ú', 'u')
                                    if 'Juarez(CHIH)' in ciudad:
                                        ciudad = 'Juarez CHIH'
                                    try:
                                        if ciudad not in table[f'{organization}_{pais}']:
                                            print(f'{ciudad} not in table')
                                            print(f'column {column}')
                                        else:
                                            suma += number*value * \
                                                table[f'{organization}_{pais}'][ciudad]
                                    except:
                                        print('organizacion', organization)
                                        print('pais', pais)
                                        print('ciudad', ciudad)
                                        print('columna', column)
                                        print('table', table)
                                        raise ValueError
                    if percentage:
                        suma = f'{suma*100}%'
                    data.append(suma)
            pais = '_'.join(list(paises2consider))
            if role == 'Farmer':
                csvData = ('Farming', organization, pais, bd)
            else:
                csvData = ('Hunting', organization, pais, bd)
            createCSV(data, *csvData)
            createTxtExplaining(bd, *csvData[0:3])


main()
