import pydantic
import src.utils.types as sc_types
from typing import Any
from pydantic import root_validator, field_validator, ValidationInfo


WEIGHT_CONVERSIONS = {
    (sc_types.Unit.GRAMS, sc_types.Unit.KILOS): 0.001,
    (sc_types.Unit.KILOS, sc_types.Unit.GRAMS): 1000.0,
    (sc_types.Unit.KILOS, sc_types.Unit.POUNDS): 2.20462,
    (sc_types.Unit.POUNDS, sc_types.Unit.KILOS): 0.453592,
    (sc_types.Unit.POUNDS, sc_types.Unit.OUNCES): 16.0,
    (sc_types.Unit.OUNCES, sc_types.Unit.POUNDS): 0.0625,
    (sc_types.Unit.OUNCES, sc_types.Unit.GRAMS): 28.3495,
    (sc_types.Unit.GRAMS, sc_types.Unit.OUNCES): 0.035274,
    (sc_types.Unit.GRAMS, sc_types.Unit.POUNDS): 0.00220462,
    (sc_types.Unit.POUNDS, sc_types.Unit.GRAMS): 453.592,
}


class Quantity(pydantic.BaseModel):
    """
    Data class representing the amount of an item.

    Attributes:
        quantity (float): The numeric value of the quantity.
        unit (sc_types.Unit): The unit of measurement.
        type (sc_types.UnitType): The type of unit (e.g., weight, volume).
    """

    quantity: float
    unit: sc_types.Unit
    type: sc_types.UnitType = pydantic.Field(
        default_factory=lambda: sc_types.UnitType.NONE
    )

    @field_validator("unit", mode="before")
    def validate_unit(cls, value):
        if isinstance(value, str):
            # Convert to lowercase and remove whitespace
            cleaned_value = value.lower().strip()

            # Try direct mapping first
            if cleaned_value in sc_types.UNIT_MAPPINGS:
                return sc_types.UNIT_MAPPINGS[cleaned_value]

            # Try enum name matching
            try:
                return sc_types.Unit[cleaned_value.upper()]
            except KeyError:
                # If no match found, default to NONE
                return sc_types.Unit.NONE
        return value

    @field_validator("type", mode="before")
    def validate_type(cls, value, info: ValidationInfo):
        # If type is explicitly provided, try to validate it
        if isinstance(value, str):
            try:
                return sc_types.UnitType[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid unit type: {value}")

        # If we have a unit, infer the type from it
        if "unit" in info.data:
            unit = cls.validate_unit(info.data["unit"])
            return sc_types.UNIT_TYPE_MAPPINGS.get(unit, sc_types.UnitType.NONE)

        return sc_types.UnitType.NONE

    @field_validator("quantity", mode="before")
    def validate_quantity(cls, value):
        if isinstance(value, dict):
            # If we receive a dictionary, extract the quantity value
            return float(value.get("quantity", 0))
        if isinstance(value, str):
            try:
                return float(value.replace(",", ""))
            except ValueError:
                raise ValueError(f"Cannot convert {value} to float")
        return float(value)

    def _check_types(self, other: "Quantity"):
        """
        Check if two Quantity objects have the same UnitType.

        Args:
            other (Quantity): The other Quantity object to compare with.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        if self.type != other.type:
            raise TypeError(
                "Quantities must have the same Unit Type to perform arithmetic."
            )

    def __add__(self, other: "Quantity") -> "Quantity":
        """
        Add two Quantity objects.

        Args:
            other (Quantity): The Quantity object to add.

        Returns:
            Quantity: A new Quantity object with the sum.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(quantity=self.quantity + value, unit=self.unit, type=self.type)

    def __iadd__(self, other: "Quantity"):
        """
        In-place addition of two Quantity objects.

        Args:
            other (Quantity): The Quantity object to add.

        Returns:
            Quantity: The updated Quantity object.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity += value
        return self

    def __sub__(self, other: "Quantity") -> "Quantity":
        """
        Subtract two Quantity objects.

        Args:
            other (Quantity): The Quantity object to subtract.

        Returns:
            Quantity: A new Quantity object with the difference.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(quantity=self.quantity - value, unit=self.unit, type=self.type)

    def __isub__(self, other: "Quantity"):
        """
        In-place subtraction of two Quantity objects.

        Args:
            other (Quantity): The Quantity object to subtract.

        Returns:
            Quantity: The updated Quantity object.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity -= value
        return self

    def __mul__(self, other: "Quantity") -> "Quantity":
        """
        Multiply two Quantity objects.

        Args:
            other (Quantity): The Quantity object to multiply by.

        Returns:
            Quantity: A new Quantity object with the product.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(quantity=self.quantity * value, unit=self.unit, type=self.type)

    def __imul__(self, other: "Quantity"):
        """
        In-place multiplication of two Quantity objects.

        Args:
            other (Quantity): The Quantity object to multiply by.

        Returns:
            Quantity: The updated Quantity object.

        Raises:
            TypeError: If the UnitTypes don't match.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity *= value
        return self

    def __truediv__(self, other: "Quantity") -> "Quantity":
        """
        Divide two Quantity objects.

        Args:
            other (Quantity): The Quantity object to divide by.

        Returns:
            Quantity: A new Quantity object with the quotient.

        Raises:
            TypeError: If the UnitTypes don't match.
            ZeroDivisionError: If the other Quantity's value is zero.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(quantity=self.quantity / value, unit=self.unit, type=self.type)

    def __itruediv__(self, other: "Quantity"):
        """
        In-place division of two Quantity objects.

        Args:
            other (Quantity): The Quantity object to divide by.

        Returns:
            Quantity: The updated Quantity object.

        Raises:
            TypeError: If the UnitTypes don't match.
            ZeroDivisionError: If the other Quantity's value is zero.
        """
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity /= value
        return self


def convert_unit(input_quantity: Quantity, output_units: sc_types.Unit) -> float:
    """
    Convert a Quantity to a different unit.

    Args:
        input_quantity (Quantity): The input Quantity object.
        output_units (sc_types.Unit): The desired output unit.

    Returns:
        float: The converted quantity value.
    """
    original_quanity = input_quantity.quantity
    original_units = input_quantity.unit

    if original_units == output_units:
        return original_quanity

    conversion_factor = _get_conversion_factor(original_units, output_units)
    return original_quanity * conversion_factor


def _get_conversion_factor(
    input_unit: sc_types.Unit, output_units: sc_types.Unit
) -> float:
    """
    Get the conversion factor between two units.

    Args:
        input_unit (sc_types.Unit): The input unit.
        output_units (sc_types.Unit): The output unit.

    Returns:
        float: The conversion factor.

    Raises:
        KeyError: If the conversion is not defined in WEIGHT_CONVERSIONS.
    """
    return WEIGHT_CONVERSIONS[(input_unit, output_units)]


def macrosDefaultDict() -> dict[sc_types.Macro, Quantity]:
    """
    Create a default dictionary of macronutrients with zero quantities.

    Returns:
        dict[sc_types.Macro, Quantity]: A dictionary with macronutrients as keys
            and zero Quantity objects as values.
    """
    return {
        sc_types.Macro.CARB: Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.FAT: Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.PROTEIN: Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.SUGAR: Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.CALORIES: Quantity(
            quantity=0, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
        ),
        sc_types.Macro.FIBER: Quantity(
            quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
        ),
    }
