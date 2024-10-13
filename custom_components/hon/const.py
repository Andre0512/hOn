from homeassistant.components.climate import (
    HVACMode,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_AUTO,
)

DOMAIN: str = "hon"
MOBILE_ID: str = "homassistant"
CONF_REFRESH_TOKEN = "refresh_token"

PLATFORMS: list[str] = [
    "sensor",
    "select",
    "number",
    "switch",
    "button",
    "binary_sensor",
    "climate",
    "fan",
    "light",
    "lock",
]

APPLIANCES: dict[str, str] = {
    "AC": "Air Conditioner",
    "AP": "Air Purifier",
    "AS": "Air Scanner",
    "DW": "Dish Washer",
    "FRE": "Freezer",
    "HO": "Hood",
    "IH": "Induction Hob",
    "MW": "Microwave",
    "OV": "Oven",
    "REF": "Fridge",
    "RVC": "Robot Vacuum Cleaner",
    "TD": "Tumble Dryer",
    "WC": "Wine Cellar",
    "WD": "Washer Dryer",
    "WH": "Water Heater",
    "WM": "Washing Machine",
}

HON_HVAC_MODE: dict[int, HVACMode] = {
    0: HVACMode.AUTO,
    1: HVACMode.COOL,
    2: HVACMode.DRY,
    3: HVACMode.DRY,
    4: HVACMode.HEAT,
    5: HVACMode.FAN_ONLY,
    6: HVACMode.FAN_ONLY,
}

HON_HVAC_PROGRAM: dict[str, str] = {
    HVACMode.AUTO: "iot_auto",
    HVACMode.COOL: "iot_cool",
    HVACMode.DRY: "iot_dry",
    HVACMode.HEAT: "iot_heat",
    HVACMode.FAN_ONLY: "iot_fan",
}

HON_FAN: dict[int, str] = {
    1: FAN_HIGH,
    2: FAN_MEDIUM,
    3: FAN_LOW,
    4: FAN_AUTO,
    5: FAN_AUTO,
}

# These languages are official supported by hOn
LANGUAGES: list[str] = [
    "ar",  # Arabic
    "bg",  # Bulgarian
    "cs",  # Czech
    "da",  # Danish
    "de",  # German
    "el",  # Greek
    "en",  # English
    "es",  # Spanish
    "fi",  # Finnish
    "fr",  # French
    "he",  # Hebrew
    "hr",  # Croatian
    "hu",  # Hungarian
    "it",  # Italian
    "nb",  # Norwegian
    "nl",  # Dutch
    "nr",  # Southern Ndebele
    "pl",  # Polish
    "pt",  # Portuguese
    "ro",  # Romanian
    "ru",  # Russian
    "sk",  # Slovak
    "sl",  # Slovenian
    "sr",  # Serbian
    "sv",  # Swedish
    "tr",  # Turkish
    "uk",  # Ukrainian
    "zh",  # Chinese
]

WASHING_PR_PHASE: dict[int, str] = {
    0: "ready",
    1: "washing",
    2: "washing",
    3: "spin",
    4: "rinse",
    5: "rinse",
    6: "rinse",
    7: "drying",
    8: "drying",
    9: "steam",
    10: "ready",
    11: "spin",
    12: "weighting",
    13: "weighting",
    14: "washing",
    15: "washing",
    16: "washing",
    17: "rinse",
    18: "rinse",
    19: "scheduled",
    20: "tumbling",
    24: "refresh",
    25: "washing",
    26: "heating",
    27: "washing",
}

MACH_MODE: dict[int, str] = {
    0: "ready",  # NO_STATE
    1: "ready",  # SELECTION_MODE
    2: "running",  # EXECUTION_MODE
    3: "pause",  # PAUSE_MODE
    4: "scheduled",  # DELAY_START_SELECTION_MODE
    5: "scheduled",  # DELAY_START_EXECUTION_MODE
    6: "error",  # ERROR_MODE
    7: "ready",  # END_MODE
    8: "test",  # TEST_MODE
    9: "ending",  # STOP_MODE
}

TUMBLE_DRYER_PR_PHASE: dict[int, str] = {
    0: "ready",
    1: "heat_stroke",
    2: "drying",
    3: "cooldown",
    8: "unknown",
    11: "ready",
    12: "unknown",
    13: "cooldown",
    14: "heat_stroke",
    15: "heat_stroke",
    16: "cooldown",
    17: "unknown",
    18: "tumbling",
    19: "drying",
    20: "drying",
}

DIRTY_LEVEL: dict[int, str] = {
    0: "unknown",
    1: "little",
    2: "normal",
    3: "very",
}

STEAM_LEVEL: dict[int, str] = {
    0: "no_steam",
    1: "cotton",
    2: "delicate",
    3: "synthetic",
}

DISHWASHER_PR_PHASE: dict[int, str] = {
    0: "ready",
    1: "prewash",
    2: "washing",
    3: "rinse",
    4: "drying",
    5: "ready",
    6: "hot_rinse",
}

TUMBLE_DRYER_DRY_LEVEL: dict[int, str] = {
    0: "no_dry",
    1: "iron_dry",
    2: "no_dry_iron",
    3: "cupboard_dry",
    4: "extra_dry",
    11: "no_dry",
    12: "iron_dry",
    13: "cupboard_dry",
    14: "ready_to_wear",
    15: "extra_dry",
}

AC_MACH_MODE: dict[int, str] = {
    0: "auto",
    1: "cool",
    2: "cool",
    3: "dry",
    4: "heat",
    5: "fan",
    6: "fan",
}

AC_FAN_MODE: dict[int, str] = {
    1: "high",
    2: "mid",
    3: "low",
    4: "auto",
    5: "auto",
}

AC_HUMAN_SENSE: dict[int, str] = {
    0: "touch_off",
    1: "avoid_touch",
    2: "follow_touch",
    3: "unknown",
}

AP_MACH_MODE: dict[int, str] = {
    1: "sleep",
    2: "auto",
    3: "allergens",
    4: "max",
}

AP_DIFFUSER_LEVEL: dict[int, str] = {
    0: "off",
    1: "soft",
    2: "mid",
    3: "h_biotics",
    4: "custom",
}

REF_HUMIDITY_LEVELS: dict[int, str] = {1: "low", 2: "mid", 3: "high"}

STAIN_TYPES: dict[int, str] = {
    0: "unknown",
    1: "wine",
    2: "grass",
    3: "soil",
    4: "blood",
    5: "milk",
    # 6: "butter",
    6: "cooking_oil",
    7: "tea",
    8: "coffee",
    # 9: "chocolate",
    9: "ice_cream",
    10: "lip_gloss",
    11: "curry",
    12: "milk_tea",
    # 13: "chili_oil",
    13: "rust",
    14: "blue_ink",
    # 14: "mech_grease",
    # 15: "color_pencil",
    # 15: "deodorant",
    15: "perfume",
    # 16: "glue",
    16: "shoe_cream",
    17: "oil_pastel",
    18: "blueberry",
    19: "sweat",
    20: "egg",
    # 20: "mayonnaise",
    21: "ketchup",
    22: "baby_food",
    23: "soy_sauce",
    24: "bean_paste",
    25: "chili_sauce",
    26: "fruit",
}

AC_POSITION_HORIZONTAL = {
    0: "position_1",
    3: "position_2",
    4: "position_3",
    5: "position_4",
    6: "position_5",
    7: "swing",
}

AC_POSITION_VERTICAL = {
    2: "position_1",
    4: "position_2",
    5: "position_3",
    6: "position_4",
    7: "position_5",
    8: "swing",
}
