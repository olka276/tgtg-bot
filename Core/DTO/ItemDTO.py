from typing import NamedTuple


class ItemDTO(NamedTuple):
    id: int
    name: str
    url: str or None
    address: str or None
    amount: int
    current_price: float
    old_price: float
    ratings: float or None
    pick_up_from: str
    pick_up_to: str
    source: str
    other_details: str or None
