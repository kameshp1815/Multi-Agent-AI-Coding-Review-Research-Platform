from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus


class AppBaseException(Exception):
    def __init__(self, error_code: str, message: str, status_code: int):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message": self.message
        }


class DatabaseConnectionException(AppBaseException):
    def __init__(self, detail: str = "Failed to connect to the database."):
        super().__init__(
            error_code=ErrorCodeStatus.get(ErrorCode.DB_CONNECTION_FAILED),
            message=detail,
            status_code=503
        )

class AgentInvocationException(AppBaseException):
    def __inti__(self,detail:str="Failed to invoke an agent"):
        super().__init__(
            error_code=ErrorCodeStatus.get(ErrorCode.AGENT_INVOKE_FAILED),
            message=detail,
            status_code=500
        )

class BuildGraphException(AppBaseException):
    def __inti__(self,detail:str="Failed to build a graph"):
        super().__init__(
            error_code=ErrorCodeStatus.get(ErrorCode.BUILD_GRAPH_FAILED),
            message=detail,
            status_code=500
        )
