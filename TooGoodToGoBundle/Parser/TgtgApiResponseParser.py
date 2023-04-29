import datetime
import maya


def parse(response):
    result = list()
    for store in response:
        item = dict()
        item['id'] = store['item']['item_id']
        item['store_name'] = store['store']['store_name']
        item['items_available'] = store['items_available']

        if item['items_available'] == 0:
            result.append(item)
            continue

        item['description'] = store['item']['description']
        item['category_picture'] = store['item']['cover_picture']['current_url']
        item['price_including_taxes'] = str(store['item']['price_including_taxes']['minor_units'])[
                                        :-(store['item']['price_including_taxes']['decimals'])] + "." + str(
            store['item']['price_including_taxes']['minor_units'])[-(
            store['item']['price_including_taxes']['decimals']):] + store['item']['price_including_taxes']['code']
        item['value_including_taxes'] = str(store['item']['value_including_taxes']['minor_units'])[
                                        :-(store['item']['value_including_taxes']['decimals'])] + "." + str(
            store['item']['value_including_taxes']['minor_units'])[-(
            store['item']['value_including_taxes']['decimals']):] + store['item']['value_including_taxes']['code']
        try:
            pickup_datetime_start = datetime.datetime.strptime(store['pickup_interval']['start'],
                                                               '%Y-%m-%dT%H:%M:%S%z').replace(
                tzinfo=datetime.timezone.utc).astimezone(tz=None)
            pickup_datetime_end = datetime.datetime.strptime(store['pickup_interval']['end'],
                                                             '%Y-%m-%dT%H:%M:%S%z').replace(
                tzinfo=datetime.timezone.utc).astimezone(tz=None)
            item['pickup_start'] = maya.parse(
                pickup_datetime_start).slang_date().capitalize() + " " + pickup_datetime_start.strftime('%H:%M')
            item['pickup_end'] = maya.parse(
                pickup_datetime_end).slang_date().capitalize() + " " + pickup_datetime_end.strftime('%H:%M')
        except KeyError:
            item['pickup_start'] = None
            item['pickup_end'] = None
        try:
            item['rating'] = round(store['item']['average_overall_rating']['average_overall_rating'], 2)
        except KeyError:
            item['rating'] = None
        result.append(item)
    return result
