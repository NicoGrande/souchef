import enum


class Unit(enum.Enum):
    POUNDS = "lbs"
    KILOS = "kg"
    GRAMS = "g"
    KCAL = "kcal"
    GALLONS = "gal"
    LITER = "L"
    OUNCES = "oz"
    NONE = ""


class UnitType(enum.Enum):
    WEIGHT = enum.auto()
    VOLUME = enum.auto()
    ENERGY = enum.auto()
    NONE = enum.auto()


class StorageType(enum.Enum):
    PANTRY = enum.auto()
    FRIDGE = enum.auto()
    FREEZER = enum.auto()


class Macro(enum.Enum):
    CARB = enum.auto()
    FAT = enum.auto()
    PROTEIN = enum.auto()
    SUGAR = enum.auto()
    CALORIES = enum.auto()
    FIBER = enum.auto()
