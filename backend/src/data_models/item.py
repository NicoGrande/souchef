import datetime
import pydantic
import typing
import uuid
from src.data_models import quantity as sc_quantity
from src.data_models import nutritional_facts as sc_nutritional_facts
from src.utils import types as sc_types


class Item(pydantic.BaseModel):
    """
    Data class representing a food item to be stored.

    Attributes:
        name (str): The name of the food item.
        quantity (sc_quantity.Quantity): The quantity of the item.
        shelf_life (datetime.timedelta): The shelf life of the item.
        storage (sc_types.StorageType): The storage type for the item.
    """

    name: str
    quantity: sc_quantity.Quantity
    shelf_life: datetime.timedelta
    storage: sc_types.StorageType
    _expiration_date: datetime.date
    _item_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _nutritional_facts = pydantic.PrivateAttr(
        default_factory=sc_nutritional_facts.NutritionalFacts
    )

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

    @property
    def item_id(self) -> uuid.UUID:
        """
        Returns the item's unique identifier.

        Returns:
            uuid.UUID: The item's unique identifier.
        """
        return self._item_id

    @property
    def expiration_date(self) -> datetime.date:
        """
        Returns the item's expiration date.

        Returns:
            datetime.date: The item's expiration date.
        """
        return self._expiration_date

    @property
    def nutritional_facts(self) -> sc_nutritional_facts.NutritionalFacts:
        """
        Returns the item's nutritional facts.

        Returns:
            sc_nutritional_facts.NutritionalFacts: The item's nutritional facts.
        """
        return self._nutritional_facts

    @nutritional_facts.setter
    def nutritional_facts(self, value: sc_nutritional_facts.NutritionalFacts):
        """
        Sets the item's nutritional facts.

        Args:
            value (sc_nutritional_facts.NutritionalFacts): The new nutritional facts.
        """
        self._nutritional_facts = value

    def get_shelf_life_remaining(self) -> int:
        """
        Calculates the remaining shelf life of the item.

        Returns:
            int: The number of days remaining in the item's shelf life.
        """
        time_delta = self._expiration_date - datetime.datetime.now().date()
        return time_delta

    @pydantic.field_validator("storage", mode="before")
    def validate_storage(cls, value):
        if isinstance(value, str):
            try:
                return sc_types.StorageType[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid storage type: {value}")
        return value

    @pydantic.field_validator("shelf_life", mode="before")
    def validate_shelf_life(cls, value: str | datetime.timedelta) -> datetime.timedelta:
        """
        Parse a shelf life string into a timedelta object.
        Handles various formats including:
        - ISO 8601 duration format (e.g., 'P1Y', 'P2M', 'P5D')
        - Natural language (e.g., '1 year', '2 months', '5 days')
        - Simple number (interpreted as days)

        Args:
            value: String representation of shelf life or timedelta object

        Returns:
            datetime.timedelta: Parsed shelf life duration

        Raises:
            ValueError: If the input string cannot be parsed
        """
        if isinstance(value, datetime.timedelta):
            return value

        if not isinstance(value, str):
            raise ValueError(f"Expected string or timedelta, got {type(value)}")

        # Try parsing as simple number (days)
        try:
            return datetime.timedelta(days=float(value))
        except ValueError:
            pass

        # Clean up the input string
        value = value.lower().strip()

        # Handle ISO 8601 duration format (e.g., P1Y, P2M, P5D)
        if value.startswith("p"):
            try:
                duration = value[1:]  # Remove 'P'
                if "y" in duration:
                    years = float(duration.replace("y", ""))
                    return datetime.timedelta(days=years * 365)
                elif "m" in duration:
                    months = float(duration.replace("m", ""))
                    return datetime.timedelta(days=months * 30)
                elif "w" in duration:
                    weeks = float(duration.replace("w", ""))
                    return datetime.timedelta(days=weeks * 7)
                elif "d" in duration:
                    days = float(duration.replace("d", ""))
                    return datetime.timedelta(days=days)
                else:
                    raise ValueError(f"Unknown time unit in: {value}")
            except ValueError as e:
                raise ValueError(
                    f"Could not parse shelf life: {value}. Error: {str(e)}"
                )

        # Handle natural language format
        try:
            # Split into number and unit, handling potential extra spaces
            parts = value.split()

            # Define unit mappings with common variations
            unit_mappings = {
                "year": 365,
                "years": 365,
                "yr": 365,
                "yrs": 365,
                "y": 365,
                "month": 30,
                "months": 30,
                "mo": 30,
                "mos": 30,
                "m": 30,
                "week": 7,
                "weeks": 7,
                "wk": 7,
                "wks": 7,
                "w": 7,
                "day": 1,
                "days": 1,
                "d": 1,
            }

            if len(parts) < 2:
                for unit_str, multiplier in unit_mappings.items():
                    if value.endswith(unit_str):
                        number = float(value[: -len(unit_str)])
                        return datetime.timedelta(days=number * multiplier)
                raise ValueError(
                    f"Could not parse shelf life: {value}. Error: {str(e)}"
                )

            else:
                number = float(parts[0])
                unit = "".join(
                    parts[1:]
                )  # Join remaining parts to handle "2 and a half years"

                # Find matching unit
                if unit not in unit_mappings:
                    raise ValueError(f"Unknown time unit in: {value}")

                multiplier = unit_mappings[unit]
                return datetime.timedelta(days=number * multiplier)

        except ValueError as e:
            raise ValueError(f"Could not parse shelf life: {value}. Error: {str(e)}")
