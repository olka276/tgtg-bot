from collections import namedtuple
from typing import NamedTuple


class ItemDTO(NamedTuple):
    id: int
    name: str
    url: str
    amount: int
    current_price: float
    old_price: float
    ratings: float or None
    pick_up_from: str
    pick_up_to: str
    source: str
    msg_id: str or None = None

    @property
    def msg_id(self):
        return self.msg_id

    @msg_id.setter
    def msg_id(self, value):
        self.msg_id = value

