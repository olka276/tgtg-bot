from TooGoodToGoBundle.Transformer import ResponseTransformer


def parse(response):
    item_data = list()
    for item in response:
        item_data.append(ResponseTransformer.transform(item))

    return item_data
