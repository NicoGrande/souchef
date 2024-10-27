import enum


class Unit(enum.Enum):
    """
    Enumeration of measurement units.

    Attributes:
        POUNDS (str): Pounds, represented as "lbs".
        KILOS (str): Kilograms, represented as "kg".
        GRAMS (str): Grams, represented as "g".
        KCAL (str): Kilocalories, represented as "kcal".
        GALLONS (str): Gallons, represented as "gal".
        LITER (str): Liters, represented as "L".
        OUNCES (str): Ounces, represented as "oz".
        NONE (str): Empty string, representing no unit.
    """

    POUNDS = "lbs"
    KILOS = "kg"
    GRAMS = "g"
    KCAL = "kcal"
    GALLONS = "gal"
    LITER = "L"
    OUNCES = "oz"
    NONE = ""


class UnitType(enum.Enum):
    """
    Enumeration of unit types.

    Attributes:
        WEIGHT: Represents weight units.
        VOLUME: Represents volume units.
        ENERGY: Represents energy units.
        NONE: Represents no specific unit type.
    """

    WEIGHT = enum.auto()
    VOLUME = enum.auto()
    ENERGY = enum.auto()
    NONE = enum.auto()


class StorageType(enum.Enum):
    """
    Enumeration of storage types for food items.

    Attributes:
        PANTRY: Represents pantry storage.
        FRIDGE: Represents refrigerator storage.
        FREEZER: Represents freezer storage.
    """

    PANTRY = enum.auto()
    FRIDGE = enum.auto()
    FREEZER = enum.auto()


class Macro(enum.Enum):
    """
    Enumeration of macronutrients and nutritional information.

    Attributes:
        CARB: Represents carbohydrates.
        FAT: Represents fats.
        PROTEIN: Represents proteins.
        SUGAR: Represents sugars.
        CALORIES: Represents calories.
        FIBER: Represents dietary fiber.
    """

    CARB = enum.auto()
    FAT = enum.auto()
    PROTEIN = enum.auto()
    SUGAR = enum.auto()
    CALORIES = enum.auto()
    FIBER = enum.auto()
