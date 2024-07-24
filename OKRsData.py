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
                             (data[column] != '-') &
                             (data[column] != '0') &
                             (data[column] != 0)]
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


plus5Orders = generalGetter('plus5orderRs.csv',
                            '5 + order store count(week total)')
newAdquireRs = generalGetter('newRsOrders.csv', 'shop_cnt')
ordersOfNewAdquireRs = generalGetter('newRsOrders.csv', 'complete_orders')
generalDailyOrders = generalGetter('generalDailyOrders.csv', 'Daily Orders')
