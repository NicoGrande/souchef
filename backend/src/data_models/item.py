import dataclasses
import uuid
import datetime

from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types


@dataclasses.dataclass
class Item:
    """Data class representing food item to be stored."""

    name: str
    item_id: uuid.UUID
    quantity: sc_quantity.Quantity
    price: float
    merchant: str
    per_unit_macros: dict[sc_types.Macro, sc_quantity.Quantity]
    expiration_date: datetime
    storage: sc_types.StorageType

    def __repr__(self):
        return self.name

    def get_shelf_life_remaining(self):
        time_delta = self.expiration_date - datetime.datetime.now().date()
        return time_delta.days
