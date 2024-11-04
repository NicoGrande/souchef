import datetime
import pydantic
import typing
import uuid
from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types
from pydantic import field_validator


class Item(pydantic.BaseModel):
    """
    Data class representing a food item to be stored.

    Attributes:
        name (str): The name of the food item.
        quantity (sc_quantity.Quantity): The quantity of the item.
        price (float): The price of the item.
        merchant (str): The merchant where the item was purchased.
        per_serving_macros (dict[sc_types.Macro, sc_quantity.Quantity]): Macronutrients per serving.
        serving_size (sc_quantity.Quantity): The size of one serving.
        shelf_life (datetime.timedelta): The shelf life of the item.
        storage (sc_types.StorageType): The storage type for the item.
    """

    name: str
    quantity: sc_quantity.Quantity
    price: float
    per_serving_macros: dict[sc_types.Macro, sc_quantity.Quantity] = pydantic.Field(
        default_factory=sc_quantity.macrosDefaultDict
    )
    serving_size: sc_quantity.Quantity
    shelf_life: datetime.timedelta
    storage: sc_types.StorageType
    _expiration_date: datetime.date
    _item_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)

    def model_post_init(self, __context: typing.Any):
        """Post-initialization method to set the expiration date."""
        self._expiration_date = datetime.datetime.now().date() + self.shelf_life

    def __repr__(self):
        """
        Returns a string representation of the Item.

        Returns:
            str: The name of the item.
        """
        return self.name

    def __hash__(self):
        """
        Computes the hash value for the Item.

        Returns:
            int: The hash value of the item's name.
        """
        return hash(self.name)

    def __eq__(self, other: "Item"):
        """
        Checks if this Item is equal to another Item.

        Args:
            other (Item): The other Item to compare with.

        Returns:
            bool: True if the items have the same name and expiration date, False otherwise.
        """
        return (
            self.name == other.name and self._expiration_date == other._expiration_date
        )

    def get_shelf_life_remaining(self) -> int:
        """
        Calculates the remaining shelf life of the item.

        Returns:
            int: The number of days remaining in the item's shelf life.
        """
        time_delta = self._expiration_date - datetime.datetime.now().date()
        return time_delta.days

    @field_validator("storage", mode="before")
    def validate_storage(cls, value):
        if isinstance(value, str):
            try:
                return sc_types.StorageType[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid storage type: {value}")
        return value

    @field_validator("per_serving_macros", mode="before")
    def validate_macros(cls, value):
        if isinstance(value, dict):
            validated_macros = {}
            for key, quantity in value.items():
                if isinstance(key, str):
                    try:
                        macro_key = sc_types.MACRO_MAPPINGS[key.lower()]
                        validated_macros[macro_key] = quantity
                    except KeyError:
                        raise ValueError(f"Invalid macro type: {key}")
                elif isinstance(key, sc_types.Macro):
                    validated_macros[key] = quantity
                else:
                    raise ValueError(f"Invalid macro type: {key}")
            return validated_macros
        return value
