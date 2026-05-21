class ErrorCode:
    DB_CONNECTION_FAILED = "DatabaseConnectionFailedErrorCode"
    INTERNAL_SERVER_ERROR = "InternalServerErrorCode"
    CHAT_PROCESSING_FAILED = "ChatProcessingFailedErrorCode"
    AGENT_INVOKE_FAILED = "AgentInvokeFailedErrorCode"
    BUILD_GRAPH_FAILED="BuildGraphFailedErrorcode"
    INVALID_REQUEST = "InvalidRequestErrorCode"


ErrorCodeStatus = {
    ErrorCode.DB_CONNECTION_FAILED: "CA_DB_001",
    ErrorCode.INTERNAL_SERVER_ERROR: "CA_SYS_001",
    ErrorCode.CHAT_PROCESSING_FAILED: "CA_CHAT_001",
    ErrorCode.AGENT_INVOKE_FAILED: "CA_AGENT_001",
    ErrorCode.INVALID_REQUEST: "CA_REQ_001",
    ErrorCode.BUILD_GRAPH_FAILED:"CA_BG_001"
}

class StatusCode:
    INTERNAL_SERVER_ERROR_STATUS_CODE=500
    RESPONSE_GENERATED_STATUS_CODE=200