from Core.DTO.ItemDTO import ItemDTO
import dateutil.parser


def transform(response_data):
    return ItemDTO(
        id=response_data["id"],
        name=response_data["name"],
        url=response_data["url"],
        address=None,
        amount=0 if response_data['package_day']['meals_left'] is None else response_data["package_day"]["meals_left"],
        current_price=response_data["meal"]["price"],
        old_price=response_data["meal"]["original_price"],
        ratings=None,
        pick_up_from=dateutil.parser.parse(response_data['package_day']['collection_day']['opened_at']).strftime('%H:%M'),
        pick_up_to=dateutil.parser.parse(response_data['package_day']['collection_day']['closed_at']).strftime('%H:%M'),
        source="Foodsi",
        other_details=None
    )
