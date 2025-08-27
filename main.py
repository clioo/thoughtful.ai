from lib.constants import PackageType
from lib.exceptions import InvalidDimensionError, InvalidInputType, InvalidMassError


def sort(width: int | float, height: int | float, length: int | float,
         mass: int | float) -> str:
    allowed_types = {int, float}
    input_types = {type(width), type(height), type(length), type(mass)}
    if not input_types.issubset(allowed_types):
        raise InvalidInputType(
            "All package dimensions must be positive values")

    # Validate input dimensions
    if width <= 0 or height <= 0 or length <= 0:
        raise InvalidDimensionError(
            "All package dimensions must be positive values")

    # Validate input mass
    if mass <= 0:
        raise InvalidMassError("Package mass must be positive value")

    # Calculate volume
    volume = width * height * length

    # Check if package is bulky
    is_bulky = False
    if volume >= 1_000_000:
        is_bulky = True
    if width >= 150 or height >= 150 or length >= 150:
        is_bulky = True

    # Check if package is heavy
    is_heavy = False
    if mass >= 20:
        is_heavy = True

    # Determine stack based on classification rules
    # REJECTED: both heavy and bulky (highest priority)
    if is_heavy and is_bulky:
        return PackageType.REJECTED

    # SPECIAL: either heavy or bulky (but not both)
    if is_heavy or is_bulky:
        return PackageType.SPECIAL

    # STANDARD: neither heavy nor bulky
    return PackageType.STANDARD


if __name__ == "__main__":
    """Run unit tests when this file is executed directly."""
    import pytest
    import sys
    import os

    print("🚀 Running package sorting unit tests...")
    print("=" * 50)

    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(current_dir, "tests", "test_main.py")

    # Run pytest with verbose output
    exit_code = pytest.main([test_file, "-v", "--tb=short", "--color=yes"])

    if exit_code == 0:
        print(
            "\n✅ All tests passed! The package sorting system is working correctly."
        )
    else:
        print(f"\n❌ Some tests failed. Exit code: {exit_code}")

    sys.exit(exit_code)
