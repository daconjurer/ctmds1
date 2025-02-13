import numpy as np

from ctmds.data_generators.raw_price import (
    normal_distribution_generator,
    random_generator,
    random_iterator,
)


def test_random_iterator():
    # Setup
    ...

    # Test
    result = [next(random_iterator()) for _ in range(10)]

    # Validation
    assert all(0 <= x < 100 for x in result)


def test_random_generator():
    # Setup
    num = 10

    # Test
    result = random_generator(num)

    # Validation
    assert len(result) == num
    assert all(isinstance(x, np.ndarray) for x in result)
    assert all(0 <= x < 100 for x in result)


def test_normal_distribution_generator():
    # Setup
    ...

    # Test
    result = normal_distribution_generator(
        base_price=10,
        periods=10,
    )

    # Validation
    assert len(result) == 10
    assert all(isinstance(x, float) for x in result)
    assert all(0 <= x < 100 for x in result)


def test_normal_distribution_generator_within_std_dev():
    # Setup
    mean = 50.0
    std_dev = 2.0
    size = 1000  # Large sample size for statistical significance

    # Test
    result = normal_distribution_generator(
        base_price=mean,
        periods=size,
    )

    # Validation
    assert len(result) == size
    assert all(isinstance(x, float) for x in result)

    # Check that values fall within 2 standard deviations (95% of values should)
    lower_bound = mean - (2 * std_dev)
    upper_bound = mean + (2 * std_dev)
    values_within_bounds = [x for x in result if lower_bound <= x <= upper_bound]

    # In a normal distribution, ~95% of values should fall within 2 standard deviations
    percentage_within_bounds = len(values_within_bounds) / size
    # Assert with an accuracy of 1%
    assert percentage_within_bounds >= 0.94, (
        f"Expected at least 95% of values to be within 2 standard deviations, "
        f"but only {percentage_within_bounds:.1%} were"
    )
