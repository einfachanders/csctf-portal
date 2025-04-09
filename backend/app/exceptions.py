from fastapi import status

class GenericJSONException(Exception):
    def __init__(self, status_code: int, json: dict):
        self.status_code= status_code
        self.json = json

class UnauthorizedException(GenericJSONException):
    def __init__(self, message: str):
        super().__init__(
            status_code = 401, 
            json= {
                "status_code": 401,
                "status_message": "Unauthorized",
                "error": message
            }
        )

class NotFoundException(GenericJSONException):
    def __init__(self, message: str):
        super().__init__(
            status_code = 404, 
            json= {
                "status_code": 404,
                "status_message": "Not found",
                "error": message
            }
        )

class BadRequestException(GenericJSONException):
    def __init__(self, message: str):
        super().__init__(
            status_code = 400, 
            json= {
                "status_code": 400,
                "status_message": "Not found",
                "error": message
            }
        )