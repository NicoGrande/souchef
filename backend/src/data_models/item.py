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
    per_serving_macros: dict[sc_types.Macro, sc_quantity.Quantity]
    serving_size: sc_quantity.Quantity
    expiration_date: datetime.datetime | None
    shelf_life: datetime.timedelta | None
    storage: sc_types.StorageType

    def __post_init__(self):
        if self.expiration_date is None and self.shelf_life is None:
            raise ValueError(
                "At lease one of expiration_date or shelf_life must be specified."
            )

        if self.expiration_date is None:
            self.expiration_date = datetime.datetime.now().date() + self.shelf_life

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other: "Item"):
        return self.name == other.name

    def get_shelf_life_remaining(self):
        if self.expiration_date is not None:
            time_delta = self.expiration_date - datetime.datetime.now().date()

        return time_delta.days
    