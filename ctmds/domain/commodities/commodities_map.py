from typing import Type

from ctmds.domain.commodities.crude import CrudeOil
from ctmds.domain.commodities.natural_gas import NaturalGas
from ctmds.domain.commodities.power import Power
from ctmds.domain.commodity.interface import CommodityInterface
from ctmds.domain.constants import SupportedCommodities


class CommodityMap:
    """Map of supported commodities to their implementations."""

    _commodity_map = {
        SupportedCommodities.CRUDE: CrudeOil,
        SupportedCommodities.NATURAL_GAS: NaturalGas,
        SupportedCommodities.POWER: Power,
    }

    @staticmethod
    def get_commodity(commodity: SupportedCommodities) -> Type[CommodityInterface]:
        """Get the commodity implementation for a given commodity."""
        return CommodityMap._commodity_map.get(commodity, SupportedCommodities.CRUDE)
