class ServiceError(Exception):
    def __init__(self, message: str, *, code: str = "service_error", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message, code="not_found", status_code=404)
