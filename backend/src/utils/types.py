import enum


class Unit(enum.Enum):
    POUNDS = "lbs"
    KILOS = "kg"
    GRAMS = "g"
    NONE = ""


class UnitType(enum.Enum):
    WEIGHT = enum.auto()
    VOLUME = enum.auto()


class Macro(enum.Enum):
    CARB = enum.auto()
    FAT = enum.auto()
    PROTEIN = enum.auto()
