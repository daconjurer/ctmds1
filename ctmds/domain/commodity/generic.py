from datetime import datetime
from typing import Callable, Dict, List, Optional

from ctmds.data_generators.daily_price import daily_prices_with_timestamps
from ctmds.domain import exceptions
from ctmds.domain.commodity.interface import CommodityInterface
from ctmds.domain.constants import CountryCodes, Granularity
from ctmds.domain.models.price import PriceCollection


class GenericCommodity(CommodityInterface):
    """Implementation of CommodityInterface for generic commodity."""

    BASE_PRICES: Dict[CountryCodes, float]

    def __init__(self, prices_generator: Callable):
        self.prices_generator = prices_generator

    def get_daily_prices(
        self,
        date: datetime,
        country_code: CountryCodes,
        granularity: Granularity,
        seed: Optional[int] = None,
    ) -> PriceCollection:
        """Get daily generic commodity prices."""
        self.validate_country_code(country_code)
        return daily_prices_with_timestamps(
            base_price=self.get_base_price(country_code),
            date=date,
            granularity=granularity,
            country_code=country_code,
            seed=seed,
            daily_prices_generator=self.prices_generator,
        )

    def get_base_price(self, country_code: CountryCodes) -> float:
        """Get base price for generic commodity in a country."""
        self.validate_country_code(country_code)
        return self.BASE_PRICES[country_code]

    def get_supported_countries(self) -> List[CountryCodes]:
        """Get list of supported country codes."""
        return list(self.BASE_PRICES.keys())

    def validate_country_code(self, country_code: CountryCodes) -> None:
        """Validate if a country code is supported."""
        if country_code not in self.BASE_PRICES:
            raise exceptions.IncorrectCountryCodeError(
                f"Country code must be one of: {', '.join(self.get_supported_countries())}"
            )
