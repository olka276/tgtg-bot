import dateutil.parser


def parse(response):
    item_data = list()
    # Go through all favorites linked to the account,that are returned with the api
    for item in response['data']:
        temp = item
        temp['opened_at'] = dateutil.parser.parse(
            item['package_day']['collection_day']['opened_at']).strftime('%H:%M')
        temp['closed_at'] = dateutil.parser.parse(
            item['package_day']['collection_day']['closed_at']).strftime('%H:%M')
        if item['package_day']['meals_left'] is None:
            temp['package_day']['meals_left'] = 0
        item_data.append(temp)

    return item_data
