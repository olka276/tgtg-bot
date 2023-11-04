from datetime import datetime, timedelta

from Core.DTO.ItemDTO import ItemDTO

def transform(response_data):
    attributes = response_data['attributes']
    return ItemDTO(
        id=response_data["id"],
        name=attributes["venue_name"],
        url=None,
        address=attributes["venue_pickup_address"],
        amount=0 if attributes["current_quantity"] is None else attributes["current_quantity"],
        current_price=attributes["unit_price"],
        old_price=attributes["original_price"],
        ratings=None,
        pick_up_from=(datetime.fromisoformat(attributes["pickup_from"]) + timedelta(hours=1)).strftime("%H:%M"),
        pick_up_to=(datetime.fromisoformat(attributes["pickup_to"]) + timedelta(hours=1)).strftime("%H:%M"),
        source="Foodsi",
        other_details=None
    )
