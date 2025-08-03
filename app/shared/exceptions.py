class BusinessException(Exception):
    """Exception raised for business logic errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundException(Exception):
    """Exception raised when a resource is not found"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationException(Exception):
    """Exception raised for validation errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(Exception):
    """Exception raised for authorization errors"""
    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(self.message)


class ConflictException(Exception):
    """Exception raised for conflict errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)