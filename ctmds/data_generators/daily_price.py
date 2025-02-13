from datetime import datetime
from typing import Callable

from pytz import country_timezones

from ctmds.data_generators.raw_price import normal_distribution_generator
from ctmds.domain.constants import CountryCodes, Granularity
from ctmds.domain.models.price import Price, PriceCollection
from ctmds.utils.date import TimezoneAwareDate


def format_time(
    input_hour: int,
    granularity: Granularity,
) -> str:
    """Format time as HHMM"""
    granular_hour = input_hour if granularity == Granularity.HOURLY else input_hour // 2
    granular_minute = 0 if granularity == Granularity.HOURLY else (input_hour % 2) * 30
    return f"{granular_hour:02d}{granular_minute:02d}"


def daily_prices_with_timestamps(
    date: datetime,
    country_code: CountryCodes,
    base_price: float,
    granularity: Granularity = Granularity.HOURLY,
    seed: int | None = None,
    daily_prices_generator: Callable = normal_distribution_generator,
) -> PriceCollection:
    """
    Generate random daily prices for a specific country and date.

    Handles DST transitions:
    - Short days (23 hours) during spring forward
    - Long days (25 hours) during fall back
    - Normal days (24 hours)

    Args:
        date: The date to generate prices for
        country_code: The country code (GB, FR, NL, DE)
        granularity: Time granularity (hourly or half-hourly)
        seed: Random seed for reproducibility
        daily_prices_generator: Function to generate the prices

    Returns:
        Collection of daily prices with timestamps
    """

    timezone = country_timezones[country_code.value][0]
    day_hours = TimezoneAwareDate(date, timezone).get_day_hours()

    # Calculate number of periods based on actual hours and granularity
    num_hours = day_hours
    periods = num_hours * 2 if granularity == Granularity.HALF_HOURLY else num_hours

    prices = daily_prices_generator(
        base_price=base_price, date=date, periods=periods, seed=seed
    )

    prices_with_timestamps = []
    for i, price in enumerate(prices):
        time_str = format_time(i, granularity)
        prices_with_timestamps.append(Price(price=price, timestamp=time_str))

    return PriceCollection(prices=prices_with_timestamps)
