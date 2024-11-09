import enum


class Unit(enum.Enum):
    """
    Enumeration of measurement units.

    Attributes:
        POUNDS (str): Pounds, represented as "lb".
        KILOS (str): Kilograms, represented as "kg".
        GRAMS (str): Grams, represented as "g".
        KCAL (str): Kilocalories, represented as "kcal".
        GALLONS (str): Gallons, represented as "gal".
        LITER (str): Liters, represented as "L".
        OUNCES (str): Ounces, represented as "oz".
        NONE (str): Empty string, representing no unit.
    """

    POUNDS = "lb"
    KILOS = "kg"
    GRAMS = "g"
    KCAL = "kcal"
    GALLONS = "gal"
    LITER = "L"
    MILLILITER = "ml"
    OUNCES = "oz"
    NONE = "none"


class UnitType(enum.Enum):
    """
    Enumeration of unit types.

    Attributes:
        WEIGHT: Represents weight units.
        VOLUME: Represents volume units.
        ENERGY: Represents energy units.
        NONE: Represents no specific unit type.
    """

    WEIGHT = "weight"
    VOLUME = "volume"
    ENERGY = "energy"
    NONE = "none"


class StorageType(enum.Enum):
    """
    Enumeration of storage types for food items.

    Attributes:
        PANTRY: Represents pantry storage.
        FRIDGE: Represents refrigerator storage.
        FREEZER: Represents freezer storage.
    """

    PANTRY = "pantry"
    FRIDGE = "fridge"
    FREEZER = "freezer"


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

    CARB = "carbohydrates"
    FAT = "fat"
    PROTEIN = "protein"
    SUGAR = "sugar"
    CALORIES = "calories"
    FIBER = "fiber"


# Common unit string mappings
UNIT_MAPPINGS = {
    # Weight units
    "g": Unit.GRAMS,
    "gram": Unit.GRAMS,
    "grams": Unit.GRAMS,
    "kg": Unit.KILOS,
    "kilo": Unit.KILOS,
    "kilos": Unit.KILOS,
    "kilogram": Unit.KILOS,
    "kilograms": Unit.KILOS,
    "lb": Unit.POUNDS,
    "lbs": Unit.POUNDS,
    "pound": Unit.POUNDS,
    "pounds": Unit.POUNDS,
    "oz": Unit.OUNCES,
    "ounce": Unit.OUNCES,
    "ounces": Unit.OUNCES,
    # Volume units
    "gal": Unit.GALLONS,
    "gallon": Unit.GALLONS,
    "gallons": Unit.GALLONS,
    "l": Unit.LITER,
    "liter": Unit.LITER,
    "liters": Unit.LITER,
    "ml": Unit.MILLILITER,
    "mls": Unit.MILLILITER,
    "milliliter": Unit.MILLILITER,
    "milliliters": Unit.MILLILITER,
    # Energy units
    "kcal": Unit.KCAL,
    "calorie": Unit.KCAL,
    "calories": Unit.KCAL,
    # Count units
    "each": Unit.NONE,
    "count": Unit.NONE,
    "piece": Unit.NONE,
    "pieces": Unit.NONE,
}

# Unit type mappings
UNIT_TYPE_MAPPINGS = {
    Unit.GRAMS: UnitType.WEIGHT,
    Unit.KILOS: UnitType.WEIGHT,
    Unit.POUNDS: UnitType.WEIGHT,
    Unit.OUNCES: UnitType.WEIGHT,
    Unit.GALLONS: UnitType.VOLUME,
    Unit.LITER: UnitType.VOLUME,
    Unit.MILLILITER: UnitType.VOLUME,
    Unit.KCAL: UnitType.ENERGY,
    Unit.NONE: UnitType.NONE,
}

MACRO_MAPPINGS = {
    # Carbohydrates
    "carbohydrates": Macro.CARB,
    "carbohydrate": Macro.CARB,
    "carbs": Macro.CARB,
    # Fat
    "fat": Macro.FAT,
    "fats": Macro.FAT,
    "total fat": Macro.FAT,
    # Protein
    "protein": Macro.PROTEIN,
    # Sugar
    "sugar": Macro.SUGAR,
    "sugars": Macro.SUGAR,
    "total sugars": Macro.SUGAR,
    # Calories
    "calories": Macro.CALORIES,
    "cals": Macro.CALORIES,
    "kcal": Macro.CALORIES,
    # Fiber
    "fiber": Macro.FIBER,
    "total fiber": Macro.FIBER,
    "dietary fiber": Macro.FIBER,
}
