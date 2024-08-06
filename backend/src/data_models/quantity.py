from dataclasses import dataclass
import backend.src.utils.types as sc_types


WEIGHT_CONVERSIONS = {
    (sc_types.Unit.GRAMS, sc_types.Unit.KILOS): 1000.0,
    (sc_types.Unit.KILOS, sc_types.Unit.GRAMS): 0.001,
    (sc_types.Unit.KILOS, sc_types.Unit.POUNDS): 2.20462,
    (sc_types.Unit.POUNDS, sc_types.Unit.KILOS): 0.453592,
}


@dataclass
class Quantity:
    """Data class representing the amount of an item."""

    quantity: float
    unit: sc_types.Unit
    type: sc_types.UnitType

    def _check_types(self, other: "Quantity"):
        if self.type != other.type:
            raise TypeError(
                "Quantities must have the same Unit Type to perform arithmetic."
            )

    def __add__(self, other: "Quantity") -> "Quantity":
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(self.quantity + value, self.unit, self.type)

    def __iadd__(self, other: "Quantity"):
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity += value

    def __sub__(self, other: "Quantity") -> "Quantity":
        self._check_types(other)
        value = convert_unit(other, self.unit)
        return Quantity(self.quantity - value, self.unit, self.type)

    def __isub__(self, other: "Quantity"):
        self._check_types(other)
        value = convert_unit(other, self.unit)
        self.quantity -= value


def convert_unit(input_quantity: Quantity, output_units: sc_types.Unit) -> float:
    original_quanity = input_quantity.quantity
    original_units = input_quantity.unit

    conversion_factor = _get_conversion_factor(original_units, output_units)
    return original_quanity * conversion_factor


def _get_conversion_factor(
    input_unit: sc_types.Unit, output_units: sc_types.Unit
) -> float:
    return WEIGHT_CONVERSIONS[(input_unit, output_units)]


def macrosDefaultDict() -> dict[sc_types.Macro, Quantity]:
    return {
        sc_types.Macro.CARB: Quantity(0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
        sc_types.Macro.FAT: Quantity(0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT),
        sc_types.Macro.PROTEIN: Quantity(
            0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.SUGAR: Quantity(
            0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
        ),
        sc_types.Macro.CALORIES: Quantity(
            0, sc_types.Unit.KCAL, sc_types.UnitType.ENERGY
        ),
        sc_types.Macro.FIBER: Quantity(
            0, sc_types.Unit.GRAMS, sc_types.UnitType.WEIGHT
        ),
    }
