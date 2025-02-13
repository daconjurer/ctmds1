import random
from datetime import datetime
from decimal import Decimal
from typing import Iterator

import numpy as np


def random_iterator() -> Iterator[Decimal]:
    yield Decimal(random.randrange(0, 9999)) / 100


def random_generator(num: int) -> np.ndarray:
    nums = np.random.randint(0, 9999, size=(num, 1)) / 100
    return nums


def normal_distribution_generator(
    base_price: float,
    date: datetime | None = None,
    periods: int = 24,
    std_dev: float = 1.0,
    seed: int | None = None,
) -> list[float]:
    """Generate random decimals representing prices, following a normal distribution"""
    if seed is not None:
        np.random.seed(seed)
    return list(np.random.normal(base_price, std_dev, periods))
