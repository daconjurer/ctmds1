from datetime import datetime
from typing import List

import numpy as np


def oil_price_generator(
    base_price: float,
    periods: int,
    date: datetime,
    seed: int | None = None,
    volatility: float = 0.002,  # 0.2% daily volatility
) -> List[float]:
    """
    Generate oil prices taking into account seasonal patterns and typical volatility.

    Features:
    - Higher prices in winter months (heating oil demand)
    - Lower prices in spring (maintenance season)
    - Moderate prices in summer (driving season)
    - Seasonal volatility patterns
    - Random walk with mean reversion

    Args:
        base_price: Base price for the commodity
        periods: Number of periods to generate
        date: The date for which to generate prices
        seed: Random seed for reproducibility
        volatility: Base volatility level

    Returns:
        List of generated prices
    """
    if seed is not None:
        np.random.seed(seed)

    # Seasonal factors (monthly adjustments)
    seasonal_factors = {
        1: 1.05,  # January   - High (winter demand)
        2: 1.03,  # February  - High
        3: 0.98,  # March     - Declining (spring maintenance)
        4: 0.97,  # April     - Low (maintenance season)
        5: 0.98,  # May       - Rising (summer approaching)
        6: 1.02,  # June      - High (summer driving)
        7: 1.03,  # July      - High (peak driving)
        8: 1.01,  # August    - Moderating
        9: 0.99,  # September - Transition
        10: 1.00,  # October   - Neutral
        11: 1.02,  # November  - Rising (winter approaching)
        12: 1.04,  # December  - High (winter demand)
    }

    # Get seasonal adjustment for this month
    month = date.month
    seasonal_adjustment = seasonal_factors[month]

    # Adjust volatility based on season
    # Higher in winter months, lower in summer
    seasonal_volatility = volatility * (
        1.2 if month in [12, 1, 2] else 0.8 if month in [6, 7, 8] else 1.0
    )

    # Generate base random walk with mean reversion
    adjusted_base = base_price * seasonal_adjustment
    prices = [adjusted_base]

    for _ in range(periods - 1):
        # Mean reversion factor (pulls price back towards adjusted base)
        mean_reversion = 0.1 * (adjusted_base - prices[-1])

        # Random component with seasonal volatility
        random_change = np.random.normal(0, seasonal_volatility * prices[-1])

        # Combine mean reversion and random walk
        new_price = prices[-1] + mean_reversion + random_change

        # Ensure price doesn't go too far from base (within ±30%)
        new_price = max(adjusted_base * 0.7, min(adjusted_base * 1.3, new_price))

        prices.append(new_price)

    return prices
