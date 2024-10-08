"""Module with constants and configurations for the Mimecast integration."""

import os

AUDITS_NAME = "Audit"

LOG_LEVEL = os.environ.get("LogLevel", "INFO")
LOGS_STARTS_WITH = "Mimecast"
LOG_FORMAT = "{}(method = {}) : {} : {}"


# *Sentinel related constants
AZURE_CLIENT_ID = os.environ.get("Azure_Client_Id", "")
AZURE_CLIENT_SECRET = os.environ.get("Azure_Client_Secret", "")
AZURE_TENANT_ID = os.environ.get("Azure_Tenant_Id", "")
WORKSPACE_KEY = os.environ.get("WorkspaceKey", "")
WORKSPACE_ID = os.environ.get("WorkspaceID", "")

# *Mimecast related constants
MIMECAST_CLIENT_ID = os.environ.get("MimecastClientID")
MIMECAST_CLIENT_SECRET = os.environ.get("MimecastClientSecret")

BASE_URL = os.environ.get("BaseURL")
ENDPOINTS = {
    "OAUTH2": "/oauth/token",
    "TTP_URL": "/api/ttp/url/get-logs",
    "SEG_DLP": "/api/dlp/get-logs",
    "AUDIT_ENDPOINT": "/api/audit/get-audit-events",
}

MAX_PAGE_SIZE = 500
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TABLE_NAME = {"TTP_URL": "Ttp_Url", "SEG_DLP": "Seg_Dlp", "Audit": "MimecastAudit"}
TTP_URL_FUNCTION_NAME = "TTP_URL"
SEG_DLP_FUNCTION_NAME = "SEG_DLP"
AUDIT_FUNCTION_NAME = "Audit"
START_DATE = os.environ.get("StartDate")
DAYS_BACK = 15
FUNCTION_APP_TIMEOUT_SECONDS = 570
VALID_PREVIOUS_DAY = 63

# *Error Messages for Exception
UNEXPECTED_ERROR_MSG = "Unexpected error : Error-{}"
HTTP_ERROR_MSG = "HTTP error : Error-{}"
REQUEST_ERROR_MSG = "Request error : Error-{}"
CONNECTION_ERROR_MSG = "Connection error : Error-{}"
KEY_ERROR_MSG = "Key error : Error-{}"
TYPE_ERROR_MSG = "Type error : Error-{}"
VALUE_ERROR_MSG = "Value error : Error-{}"
JSON_DECODE_ERROR_MSG = "JSONDecode error : Error-{}"


# *checkpoint related constants
CONN_STRING = os.environ.get("AzureWebJobsStorage")
FILE_PATH = "Audit"
FILE_SHARE_NAME = os.environ.get("FileShareName")


# *Extra constants
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
MAX_FILE_SIZE = 20 * 1024 * 1024
MAX_CHUNK_SIZE = 1024 * 1024
MAX_RETRIES = 3
