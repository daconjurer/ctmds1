from typing import Dict

from ctmds.domain.commodity.generic import GenericCommodity
from ctmds.domain.constants import CountryCodes


class NaturalGas(GenericCommodity):
    """Implementation of CommodityInterface for natural gas."""

    BASE_PRICES: Dict[CountryCodes, float] = {
        CountryCodes.GB: 2.67,  # GBP/MMBtu
        CountryCodes.FR: 3.21,  # EUR/MMBtu
        CountryCodes.NL: 3.21,  # EUR/MMBtu
        CountryCodes.DE: 3.21,  # EUR/MMBtu
    }
