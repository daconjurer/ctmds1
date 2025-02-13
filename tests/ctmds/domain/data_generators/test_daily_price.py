from datetime import datetime

import pytest

from ctmds.data_generators.daily_price import daily_prices_with_timestamps
from ctmds.domain.constants import CountryCodes, Granularity


def test_daily_prices_with_timestamps_hourly():
    # Setup
    country_code = CountryCodes.GB
    for_date = datetime.now()
    granularity = Granularity.HOURLY
    seed = 123

    # Test
    result = daily_prices_with_timestamps(
        date=for_date,
        country_code=country_code,
        base_price=100,
        granularity=granularity,
        seed=seed,
    )

    # Validation
    assert len(result.prices) == 24
    assert all(isinstance(x.price, float) for x in result.prices)
    assert all(90 <= x.price < 110 for x in result.prices)

    # Check that the timestamps are in the correct format
    assert all(len(x.timestamp) == 4 for x in result.prices)
    assert all(x.timestamp.isdigit() for x in result.prices)


def test_daily_prices_with_timestamps_half_hourly():
    # Setup
    country_code = CountryCodes.GB
    for_date = datetime.now()
    granularity = Granularity.HALF_HOURLY
    seed = 123

    # Test
    result = daily_prices_with_timestamps(
        date=for_date,
        country_code=country_code,
        base_price=100,
        granularity=granularity,
        seed=seed,
    )

    # Validation
    assert len(result.prices) == 48
    assert all(isinstance(x.price, float) for x in result.prices)
    assert all(90 <= x.price < 110 for x in result.prices)

    # Check that the timestamps are in the correct format
    assert all(len(x.timestamp) == 4 for x in result.prices)
    assert all(x.timestamp.isdigit() for x in result.prices)


@pytest.mark.parametrize(
    "country_code,dst_dates",
    [
        (
            CountryCodes.GB,
            {
                "short_day": "2024-03-31",  # British Summer Time starts
                "long_day": "2024-10-27",  # British Summer Time ends
                "normal_day": "2024-06-15",
            },
        ),
        (
            CountryCodes.FR,
            {
                "short_day": "2024-03-31",  # Central European Summer Time starts
                "long_day": "2024-10-27",  # Central European Summer Time ends
                "normal_day": "2024-06-15",
            },
        ),
        (
            CountryCodes.NL,
            {
                "short_day": "2024-03-31",  # Central European Summer Time starts
                "long_day": "2024-10-27",  # Central European Summer Time ends
                "normal_day": "2024-06-15",
            },
        ),
        (
            CountryCodes.DE,
            {
                "short_day": "2024-03-31",  # Central European Summer Time starts
                "long_day": "2024-10-27",  # Central European Summer Time ends
                "normal_day": "2024-06-15",
            },
        ),
    ],
)
def test_dst_transitions(country_code: CountryCodes, dst_dates: dict[str, str]):
    # Test short day (spring forward)
    short_day = datetime.strptime(dst_dates["short_day"], "%Y-%m-%d")
    prices_short = daily_prices_with_timestamps(
        date=short_day,
        country_code=country_code,
        base_price=100,
        granularity=Granularity.HOURLY,
    )
    print(prices_short)
    assert len(prices_short.prices) == 23, "DST start should have 23 hours"

    # Test long day (fall back)
    long_day = datetime.strptime(dst_dates["long_day"], "%Y-%m-%d")
    prices_long = daily_prices_with_timestamps(
        date=long_day,
        country_code=country_code,
        base_price=100,
        granularity=Granularity.HOURLY,
    )
    assert len(prices_long.prices) == 25, "DST end should have 25 hours"

    # Test normal day
    normal_day = datetime.strptime(dst_dates["normal_day"], "%Y-%m-%d")
    prices_normal = daily_prices_with_timestamps(
        date=normal_day,
        country_code=country_code,
        base_price=100,
        granularity=Granularity.HOURLY,
    )
    assert len(prices_normal.prices) == 24, "Normal day should have 24 hours"


def test_half_hourly_dst_transitions():
    # Test half-hourly granularity during DST transition
    date = datetime.strptime("2024-03-31", "%Y-%m-%d")  # BST starts
    prices = daily_prices_with_timestamps(
        date=date,
        country_code=CountryCodes.GB,
        base_price=100,
        granularity=Granularity.HALF_HOURLY,
    )
    assert len(prices.prices) == 46, "Short day should have 46 half-hour periods"


def test_timestamp_format():
    date = datetime.strptime("2024-06-15", "%Y-%m-%d")
    prices = daily_prices_with_timestamps(
        date=date,
        country_code=CountryCodes.GB,
        base_price=100,
        granularity=Granularity.HOURLY,
    )

    # Check first and last timestamps
    assert prices.prices[0].timestamp == "0000"
    assert prices.prices[-1].timestamp == "2300"
