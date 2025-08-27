"""Custom exceptions for package sorting validation."""


class InvalidDimensionError(ValueError):
    """Raised when package dimensions are zero or negative."""
    
    def __init__(self, message: str = "Package dimensions must be positive values") -> None:
        super().__init__(message)


class InvalidMassError(ValueError):
    """Raised when package mass is zero or negative."""
    
    def __init__(self, message: str = "Package mass must be positive value") -> None:
        super().__init__(message)


class InvalidInputType(ValueError):
    """Raised when package dimensions are of invalid type."""
    
    def __init__(self, message: str = "Package dimensions must be positive values") -> None:
        super().__init__(message)
