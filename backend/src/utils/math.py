import backend.src.data_models.quantity as sc_quantity
import backend.src.utils.types as sc_types

WEIGHT_CONVERSIONS = {
    (sc_types.Unit.GRAMS, sc_types.Unit.KILOS): 1000.0,
    (sc_types.Unit.KILOS, sc_types.Unit.GRAMS): 0.001,
    (sc_types.Unit.KILOS, sc_types.Unit.POUNDS): 2.20462,
    (sc_types.Unit.POUNDS, sc_types.Unit.KILOS): 0.453592,
}


def convert_unit(input_quantity: sc_quantity.Quantity, output_units: sc_types.Unit):
    original_quanity = input_quantity.quantity
    original_units = input_quantity.unit

    conversion_factor = _get_conversion(original_units, output_units)
    return original_quanity * conversion_factor


def _get_conversion(input_unit: sc_types.Unit, output_units: sc_types.Unit):
    return WEIGHT_CONVERSIONS[(input_unit, output_units)]
