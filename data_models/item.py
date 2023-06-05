from dataclasses import dataclass
from uuid import UUID
from quantity import Quantity


@dataclass
class Item:
    """Class representing food item to be stored."""

    name: str
    item_id: UUID
    quantity: Quantity
    unit_price: float
    merchant: str
    nutritional_facts: dict[str, str]
    shelf_life_pantry: str
    shelf_life_refrigerated: str
    shelf_life_frozen: str
    is_refrigerated: bool
    is_frozen: bool
