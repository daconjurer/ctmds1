from datetime import datetime
from typing import List

import numpy as np


def gas_price_generator(
    base_price: float,
    periods: int,
    date: datetime,
    seed: int | None = None,
    volatility: float = 0.03,  # 3% daily volatility
) -> List[float]:
    """
    Generate natural gas prices with seasonal patterns.

    Features:
    - Strong seasonal pattern (winter heating)
    - Storage level impacts
    - Weekend effects
    - Weather sensitivity
    - Less intraday variation than power

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
        1: 1.20,  # January   - Peak winter
        2: 1.15,  # February  - High winter
        3: 1.05,  # March     - Late winter
        4: 0.90,  # April     - Spring
        5: 0.85,  # May       - Low demand
        6: 0.80,  # June      - Summer low
        7: 0.85,  # July      - Summer
        8: 0.85,  # August    - Summer
        9: 0.90,  # September - Storage building
        10: 1.00,  # October   - Heating starts
        11: 1.10,  # November  - Early winter
        12: 1.15,  # December  - Winter
    }

    # Daily pattern factors (less pronounced than power)
    hourly_factors = {
        0: 0.95,
        1: 0.95,
        2: 0.95,
        3: 0.95,  # Night
        4: 1.0,
        5: 1.05,
        6: 1.1,
        7: 1.1,  # Morning
        8: 1.05,
        9: 1.0,
        10: 1.0,
        11: 1.0,  # Day
        12: 1.0,
        13: 1.0,
        14: 1.0,
        15: 1.0,  # Day
        16: 1.05,
        17: 1.1,
        18: 1.1,
        19: 1.05,  # Evening
        20: 1.0,
        21: 1.0,
        22: 0.95,
        23: 0.95,  # Night
    }

    # Weekend adjustment
    is_weekend = date.weekday() >= 5
    weekend_factor = 0.9 if is_weekend else 1.0

    # Get seasonal adjustment
    month = date.month
    seasonal_adjustment = seasonal_factors[month]

    # Adjust volatility based on season
    seasonal_volatility = volatility * (
        1.4
        if month in [12, 1, 2]
        # Higher in winter
        else 0.8
        if month in [6, 7, 8]
        # Lower in summer
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
        if np.random.random() < 0.01:  # 1% chance of price spike
            spike_multiplier = np.random.uniform(1.3, 2.5)
            random_change = np.random.normal(
                0, seasonal_volatility * hour_base * spike_multiplier
            )
        else:
            random_change = np.random.normal(0, seasonal_volatility * hour_base)

        price = hour_base + random_change

        # Ensure price doesn't go negative or too high
        price = max(hour_base * 0.2, min(hour_base * 3.0, price))

        prices.append(price)

    return prices
