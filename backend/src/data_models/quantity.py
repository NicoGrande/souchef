from dataclasses import dataclass
import backend.src.utils.types as sc_types


@dataclass
class Quantity:
    """Data class representing the amount of an item."""

    quantity: float
    unit: sc_types.Unit
    type: sc_types.UnitType
