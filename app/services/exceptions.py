class ServiceError(Exception):
    """Base service-layer exception."""


class ServiceDatabaseError(ServiceError):
    """Raised when a database operation fails unexpectedly."""


class ServiceConflictError(ServiceError):
    """Raised when a write conflicts with DB constraints."""
