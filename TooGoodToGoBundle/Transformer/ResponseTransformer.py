import datetime
from Core.DTO.ItemDTO import ItemDTO


def get_current_price(response_data):
    return str(
        response_data['item']['price_including_taxes']['minor_units'])[
           :-(response_data['item']['price_including_taxes']['decimals'])] + "." + str(
        response_data['item']['price_including_taxes']['minor_units'])[-(
        response_data['item']['price_including_taxes']['decimals']):] + response_data['item']['price_including_taxes'][
        'code']


def get_old_price(response_data):
    return str(response_data['item']['value_including_taxes']['minor_units'])[
           :-(response_data['item']['value_including_taxes']['decimals'])] + "." + str(
        response_data['item']['value_including_taxes']['minor_units'])[-(
        response_data['item']['value_including_taxes']['decimals']):] + response_data['item']['value_including_taxes'][
        'code']


def get_pickup_time(dtime: str or None):
    if dtime is not None:
        date = datetime.datetime.strptime(dtime, "%Y-%m-%dT%H:%M:%SZ")
        return date.strftime("%H:%M")


def get_details(response_data):
    try:
        return response_data["item"]["collection_info"]
    except KeyError:
        return None


def transform(response_data):
    ratings_data = response_data.get("item", {}).get('average_overall_rating', {}).get('average_overall_rating', None)
    return ItemDTO(
        id=response_data['item']['item_id'],
        name=response_data["display_name"],
        address=response_data["pickup_location"]["address"]["address_line"].split(",")[0],
        url=f"https://share.toogoodtogo.com/item/{response_data['item']['item_id']}",
        amount=response_data["items_available"],
        other_details=get_details(response_data),
        current_price=get_current_price(response_data),
        old_price=get_old_price(response_data),
        ratings=round(ratings_data, 2) if ratings_data is not None else None,
        pick_up_from=get_pickup_time(response_data.get("pickup_interval", {}).get('start', None)),
        pick_up_to=get_pickup_time(response_data.get("pickup_interval", {}).get('end', None)),
        source="TooGoodToGo"
    )
