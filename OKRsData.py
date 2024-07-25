import pandas as pd
from pprint import pprint


def prettifyName(name):
    name = name.replace('á', 'a').replace('é', 'e').replace(
        'í', 'i').replace('ó', 'o').replace('ú', 'u')
    if name == 'Bogota, D.C.':
        return 'Bogota D.C.'
    if name == 'Juarez(CHIH)':
        return 'Juarez CHIH'
    if 'Juarez(CHIH)' in name:
        city = 'Juarez CHIH'
    return name


def generalGetter(file, column) -> dict:
    data = pd.read_csv(file)
    data['city_name'] = data['city_name'].apply(prettifyName)
    result = {}
    for organization_type in ['SME', 'CKA']:
        for country in ['MX', 'CO', 'CR', 'PE']:
            smallData = data[(data['organization_type'] == organization_type) &
                             (data['country_code'] == country) &
                             (data[column].notna()) &
                             (data[column] != '-')]
            sumaGrande = 0
            for i, x in smallData.iterrows():
                sumaGrande += float(x[column])

            cities = smallData['city_name'].apply(prettifyName).unique()
            percentage = {}
            for city in cities:
                cityData = smallData[smallData['city_name'] == city]
                sumaChiquita = 0
                for i, x in cityData.iterrows():
                    sumaChiquita += float(x[column])
                percentage[city] = (sumaChiquita / sumaGrande)
            result[f'{organization_type}_{country}'] = percentage
    return result


def calculateRegion(ciudad, country):
    dfRegion = pd.read_csv('MX_city_region.csv')
    city = ciudad
    if country == 'MX':
        city = prettifyName(city)
        try:
            region = dfRegion[dfRegion['city_name']
                              == city]['region'].values[0]
            return region
        except:
            return None
    else:
        return city


def generatePerRegion(file, column) -> dict:
    finalData: dict = {}
    data = generalGetter(file, column)
    for key, dictOfCitiesAndPercentages in data.items():
        organization, country = key.split('_')
        for city, percentage in dictOfCitiesAndPercentages.items():
            region = calculateRegion(city, country)
            if organization not in finalData:
                finalData[organization] = {}
            if country not in finalData[organization]:
                finalData[organization][country] = {}
            if region not in finalData[organization][country]:
                finalData[organization][country][region] = 0
            finalData[organization][country][region] += percentage
    # quitar ciudades de col que no están en lso otros datos
    regions_to_remove = []
    for organization, dictOfCountries in finalData.items():
        for country, dictOfRegions in dictOfCountries.items():
            for region, percentage in dictOfRegions.items():
                if region not in ['Bogota D.C.', 'Medellin', 'Barranquilla', 'Cucuta', 'Cali'] and country == 'CO':
                    regions_to_remove.append((organization, country, region))

    for organization, country, region in regions_to_remove:
        del finalData[organization][country][region]
    # ahora a normalizar por si falta data
    for organization, dictOfCountries in finalData.items():
        for country, dictOfRegions in dictOfCountries.items():
            sumaGrande = 0
            for region, percentage in dictOfRegions.items():
                sumaGrande += percentage
            for region, percentage in dictOfRegions.items():
                finalData[organization][country][region] = percentage / sumaGrande
    return finalData


plus5Orders = generalGetter('plus5orderRs.csv',
                            '5 + order store count(week total)')
newAdquireRs = generalGetter('newRsOrders.csv', 'shop_cnt')
ordersOfNewAdquireRs = generalGetter('newRsOrders.csv', 'complete_orders')
generalDailyOrders = generalGetter('generalDailyOrders.csv', 'Daily Orders')

plus5OrdersRegion = generatePerRegion(
    'plus5orderRs.csv', '5 + order store count(week total)')
newAdquireRsRegion = generatePerRegion('newRsOrders.csv', 'shop_cnt')
ordersOfNewAdquireRsRegion = generatePerRegion(
    'newRsOrders.csv', 'complete_orders')
generalDailyOrdersRegion = generatePerRegion(
    'generalDailyOrders.csv', 'Daily Orders')
# pprint(generalDailyOrdersRegion)
