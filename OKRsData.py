import pandas as pd
from pprint import pprint


def generalGetter(file, column) -> dict:
    data = pd.read_csv(file)
    result = {}
    for organization_type in ['SME', 'CKA']:
        for country in ['MX', 'CO', 'CR', 'PE']:
            smallData = data[data['organization_type'] == organization_type]
            smallData = smallData[smallData['country_code'] == country]
            smallData[column] = smallData[column].replace(
                to_replace='-', value=0, regex=True)
            smallData[column] = pd.to_numeric(
                smallData[column], errors='coerce').fillna(0)
            totalStoresInThatCountry = smallData[column].sum(
            )

            cities = smallData['city_name'].unique()
            percentage = {}
            for city in cities:
                if 'ogot' in city:
                    city = 'Bogotá D.C.'
                if 'Juarez(CHIH)' in city:
                    city = 'Juarez CHIH'
                if 'á' in city:
                    city = city.replace('á', 'a')
                if 'é' in city:
                    city = city.replace('é', 'e')
                if 'í' in city:
                    city = city.replace('í', 'i')
                if 'ó' in city:
                    city = city.replace('ó', 'o')
                if 'ú' in city:
                    city = city.replace('ú', 'u')
                if 'ú' in city:
                    city = city.replace('ú', 'u')

                cityData = smallData[smallData['city_name'] == city]
                cityStores = cityData[column].sum(
                )
                percentage[city] = float(
                    float(cityStores) / float(totalStoresInThatCountry))
            result[f'{organization_type}_{country}'] = percentage
    return result


plus5Orders = generalGetter('plus5orderRs.csv',
                            '5 + order store count(week total)')
newAdquireRs = generalGetter('newRsOrders.csv', 'shop_cnt')
ordersOfNewAdquireRs = generalGetter('newRsOrders.csv', 'complete_orders')
generalDailyOrders = generalGetter('generalDailyOrders.csv', 'Daily Orders')
