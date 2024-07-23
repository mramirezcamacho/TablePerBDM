import pandas as pd
from pprint import pprint


def generalGetter(file, column) -> dict:
    data = pd.read_csv(file)
    result = {}
    for organization_type in ['SME', 'CKA']:
        for country in ['MX', 'CO', 'CR', 'PE']:
            smallData = data[data['organization_type'] == organization_type]
            smallData = smallData[smallData['country_code'] == country]
            totalStoresInThatCountry = smallData[column].sum(
            )
            cities = smallData['city_name'].unique()
            percentage = {}
            for city in cities:
                cityData = smallData[smallData['city_name'] == city]
                cityStores = cityData[column].sum(
                )
                percentage[city] = float(
                    float(cityStores) / float(totalStoresInThatCountry))
            result[f'{organization_type}-{country}'] = percentage
    return result


plus5Orders = generalGetter('plus5orderRs.csv',
                            '5 + order store count(week total)')
newAdquireRs = generalGetter('newRsOrders.csv', 'shop_cnt')
ordersOfNewAdquireRs = generalGetter('newRsOrders.csv', 'complete_orders')
