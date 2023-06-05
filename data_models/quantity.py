from dataclasses import dataclass
from enum import Enum


class Units(Enum):
    POUNDS = "lbs"
    KILOS = "kg"
    GRAMS = "g"
    NONE = ""


@dataclass
class Quantity:
    quantity: float
    unit: Units
