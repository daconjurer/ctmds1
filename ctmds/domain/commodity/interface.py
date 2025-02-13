from datetime import datetime
from typing import Optional, Protocol

from ctmds.domain.constants import CountryCodes, Granularity
from ctmds.domain.models.price import PriceCollection


class CommodityInterface(Protocol):
    """Protocol defining the interface for commodities."""

    def get_daily_prices(
        self,
        date: datetime,
        country_code: CountryCodes,
        granularity: Granularity,
        seed: Optional[int] = None,
    ) -> PriceCollection:
        """
        Get daily prices for the commodity.

        Args:
            date: The date to get prices for
            country_code: The country code (e.g., 'GB', 'FR')
            seed: Optional random seed for reproducibility

        Returns:
            Collection of daily prices with timestamps

        Raises:
            IncorrectCountryCodeError: If country_code is not supported
        """
        ...
