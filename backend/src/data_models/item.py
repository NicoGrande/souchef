import dataclasses
import uuid
import datetime

import backend.src.data_models.quantity as sc_quantity
import backend.src.utils.types as sc_types


@dataclasses.dataclass
class Item:
    """Data class representing food item to be stored."""

    name: str
    item_id: uuid.UUID
    quantity: sc_quantity.Quantity
    price: float
    merchant: str
    macros: dict[sc_types.Macros, sc_quantity.Quantity]
    expiration_date: datetime
    is_ingredient: bool
    is_refrigerated: bool
    is_frozen: bool
