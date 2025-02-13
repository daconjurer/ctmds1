from datetime import datetime
from typing import List

import numpy as np


def power_price_generator(
    base_price: float,
    periods: int,
    date: datetime,
    seed: int | None = None,
    volatility: float = 0.05,  # 5% base volatility (higher than oil)
) -> List[float]:
    """
    Generate electricity prices with daily and seasonal patterns.

    Features:
    - Daily peaks (morning and evening)
    - Weekend vs weekday patterns
    - Seasonal demand variations
    - Higher volatility than other commodities
    - Extreme price spikes possible

    Args:
        base_price: Base price for the commodity
        periods: Number of periods to generate
        date: The date for which to generate prices
        seed: Random seed for reproducibility
        volatility: Base volatility level
    """
    if seed is not None:
        np.random.seed(seed)

    # Seasonal factors (monthly adjustments)
    seasonal_factors = {
        1: 1.15,  # January   - High (winter heating)
        2: 1.10,  # February  - High
        3: 1.00,  # March     - Moderate
        4: 0.90,  # April     - Low (spring)
        5: 0.85,  # May       - Low
        6: 0.95,  # June      - Rising (AC demand)
        7: 1.10,  # July      - High (peak AC)
        8: 1.05,  # August    - High (AC)
        9: 0.90,  # September - Moderate
        10: 0.95,  # October   - Rising
        11: 1.05,  # November  - High
        12: 1.15,  # December  - Highest (winter peak)
    }

    # Daily pattern factors (24 hours)
    hourly_factors = {
        0: 0.7,
        1: 0.65,
        2: 0.6,
        3: 0.6,  # Night (low demand)
        4: 0.7,
        5: 0.8,
        6: 1.0,
        7: 1.3,  # Morning ramp
        8: 1.4,
        9: 1.3,
        10: 1.2,
        11: 1.1,  # Morning peak
        12: 1.0,
        13: 0.9,
        14: 0.9,
        15: 0.95,  # Afternoon
        16: 1.1,
        17: 1.4,
        18: 1.5,
        19: 1.4,  # Evening peak
        20: 1.2,
        21: 1.0,
        22: 0.9,
        23: 0.8,  # Evening decline
    }

    # Weekend adjustment (lower demand)
    is_weekend = date.weekday() >= 5
    weekend_factor = 0.8 if is_weekend else 1.0

    # Get seasonal adjustment
    month = date.month
    seasonal_adjustment = seasonal_factors[month]

    # Adjust volatility based on season and time
    seasonal_volatility = volatility * (
        1.3
        if month in [12, 1, 2, 7, 8]
        # Higher in peak seasons
        else 1.0
    )

    prices = []
    adjusted_base = base_price * seasonal_adjustment * weekend_factor

    for i in range(periods):
        hour = i % 24
        hourly_adjustment = hourly_factors[hour]

        # Base price for this hour
        hour_base = adjusted_base * hourly_adjustment

        # Add random component with possibility of price spikes
        if np.random.random() < 0.02:  # 2% chance of price spike
            spike_multiplier = np.random.uniform(1.5, 3.0)
            random_change = np.random.normal(
                0, seasonal_volatility * hour_base * spike_multiplier
            )
        else:
            random_change = np.random.normal(0, seasonal_volatility * hour_base)

        price = hour_base + random_change

        # Ensure price doesn't go negative
        price = max(price, hour_base * 0.1)

        prices.append(price)

    return prices
