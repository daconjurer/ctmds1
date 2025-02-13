from enum import Enum


class Granularity(str, Enum):
    HOURLY = "h"
    HALF_HOURLY = "hh"


class CountryCodes(str, Enum):
    GB = "GB"
    FR = "FR"
    NL = "NL"
    DE = "DE"


class SupportedCommodities(str, Enum):
    CRUDE = "crude"
    NATURAL_GAS = "natgas"
    POWER = "power"
