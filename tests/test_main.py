import pytest
from main import sort
from lib.exceptions import InvalidDimensionError, InvalidMassError, InvalidInputType
from lib.constants import PackageType


def test_normal_standard_package():
    result = sort(10, 10, 10, 5)
    assert result == PackageType.STANDARD

def test_just_under_bulky_thresholds():
    # Volume just under 1,000,000 and all dimensions under 150
    result = sort(99, 99, 99, 5)  # volume = 970,299
    assert result == PackageType.STANDARD

def test_just_under_heavy_threshold():
    result = sort(10, 10, 10, 19.9)
    assert result == PackageType.STANDARD

def test_bulky_by_volume_only():
    result = sort(100, 100, 100, 10)  # volume = 1,000,000
    assert result == PackageType.SPECIAL

def test_bulky_by_dimension_width():
    result = sort(150, 1, 1, 10)  # volume = 150, width = 150
    assert result == PackageType.SPECIAL

def test_bulky_by_dimension_height():
    result = sort(1, 150, 1, 10)  # volume = 150, height = 150
    assert result == PackageType.SPECIAL

def test_bulky_by_dimension_length():
    result = sort(1, 1, 150, 10)  # volume = 150, length = 150
    assert result == PackageType.SPECIAL

def test_heavy_only():
    result = sort(10, 10, 10, 20)  # volume = 1,000, mass = 20
    assert result == PackageType.SPECIAL

def test_very_heavy_not_bulky():
    result = sort(10, 10, 10, 50)
    assert result == PackageType.SPECIAL

def test_bulky_by_large_volume_small_dimensions():
    result = sort(101, 101, 101, 10)  # volume = 1,030,301, all dims < 150
    assert result == PackageType.SPECIAL

def test_both_heavy_and_bulky_by_volume():
    result = sort(100, 100, 100, 25)  # volume = 1,000,000, mass = 25
    assert result == PackageType.REJECTED

def test_both_heavy_and_bulky_by_dimension():
    result = sort(150, 10, 10, 20)  # width = 150, mass = 20
    assert result == PackageType.REJECTED

def test_very_large_and_very_heavy():
    result = sort(200, 200, 200, 100)
    assert result == PackageType.REJECTED

def test_exact_volume_threshold():
    result = sort(100, 100, 100, 10)  # volume = 1,000,000 exactly
    assert result == PackageType.SPECIAL

def test_one_below_volume_threshold():
    result = sort(99, 100, 100, 10)  # volume = 990,000
    assert result == PackageType.STANDARD

def test_exact_dimension_threshold():
    result = sort(150, 10, 10, 10)  # width = 150 exactly
    assert result == PackageType.SPECIAL

def test_one_below_dimension_threshold():
    result = sort(149, 10, 10, 10)  # width = 149
    assert result == PackageType.STANDARD

def test_exact_mass_threshold():
    result = sort(10, 10, 10, 20)  # mass = 20 exactly
    assert result == PackageType.SPECIAL

def test_one_below_mass_threshold():
    result = sort(10, 10, 10, 19.99)  # mass = 19.99
    assert result == PackageType.STANDARD

def test_float_dimensions_bulky_volume():
    result = sort(100.1, 100.1, 100.1, 10)  # volume ≈ 1,003,003
    assert result == PackageType.SPECIAL

def test_float_mass_heavy():
    result = sort(10, 10, 10, 20.01)
    assert result == PackageType.SPECIAL

def test_float_dimension_at_threshold():
    result = sort(150.0, 10, 10, 10)
    assert result == PackageType.SPECIAL

def test_low_volume_but_large_dimension():
    result = sort(150, 1, 1, 5)  # volume = 150, but width = 150
    assert result == PackageType.SPECIAL

def test_zero_volume_but_large_dimension():
    result = sort(150, 0.1, 0.1, 5)  # volume = 1.5, but width = 150
    assert result == PackageType.SPECIAL

def test_high_volume_small_dimensions():
    result = sort(100, 100, 100, 5)  # volume = 1,000,000, all dims < 150
    assert result == PackageType.SPECIAL

def test_zero_width_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(0, 10, 10, 5)

def test_zero_height_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(10, 0, 10, 5)

def test_zero_length_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(10, 10, 0, 5)

def test_negative_width_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(-10, 10, 10, 5)

def test_negative_height_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(10, -10, 10, 5)

def test_negative_length_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(10, 10, -10, 5)

def test_zero_mass_raises_exception():
    with pytest.raises(InvalidMassError):
        sort(10, 10, 10, 0)

def test_negative_mass_raises_exception():
    with pytest.raises(InvalidMassError):
            sort(10, 10, 10, -5)

def test_multiple_zero_dimensions_raises_exception():
    with pytest.raises(InvalidDimensionError):
        sort(0, 0, 10, 5)

def test_rejected_priority_over_special():
    result = sort(150, 150, 150, 25)
    assert result == PackageType.REJECTED

def test_special_when_only_heavy():
    result = sort(10, 10, 10, 25)
    assert result == PackageType.SPECIAL

def test_special_when_only_bulky():
    result = sort(150, 10, 10, 5)
    assert result == PackageType.SPECIAL

def test_string_width_raises_exception():
    with pytest.raises(InvalidInputType):
        sort("10", 10, 10, 5)

def test_string_height_raises_exception():
    with pytest.raises(InvalidInputType):
        sort(10, "10", 10, 5)

def test_string_length_raises_exception():
    with pytest.raises(InvalidInputType):
        sort(10, 10, "10", 5)

def test_string_mass_raises_exception():
    with pytest.raises(InvalidInputType):
        sort(10, 10, 10, "5")
