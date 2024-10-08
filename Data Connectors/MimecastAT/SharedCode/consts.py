"""Module with constants and configurations for the Mimecast integration."""

import os

LOG_LEVEL = os.environ.get("LogLevel", "INFO")
LOGS_STARTS_WITH = "Mimecast"
LOG_FORMAT = "{}(method = {}) : {} : {}"


# *Sentinel related constants
WORKSPACE_KEY = os.environ.get("WorkspaceKey", "")
WORKSPACE_ID = os.environ.get("WorkspaceID", "")
FUNCTION_APP_TIMEOUT_SECONDS = 570

# *Mimecast related constants
MIMECAST_CLIENT_ID = os.environ.get("MimecastClientID", "")
MIMECAST_CLIENT_SECRET = os.environ.get("MimecastClientSecret", "")
MAX_PAGE_SIZE = 500
BASE_URL = os.environ.get("BaseURL", "")
ENDPOINTS = {
    "OAUTH2": "/oauth/token",
    "PERFORMANCE_DETAILS": "/api/awareness-training/company/get-performance-details",
    "WATCHLIST_DETAILS": "/api/awareness-training/company/get-watchlist-details",
    "SAFE_SCORE_DETAILS": "/api/awareness-training/company/get-safe-score-details",
    "CAMPAIGN_DATA": "/api/awareness-training/phishing/campaign/get-campaign",
    "USER_DATA": "/api/awareness-training/phishing/campaign/get-user-data",
}

TABLE_NAME = {
    "PERFORMANCE_DETAILS": "Awareness_Performance_Details",
    "USER_DATA": "Awareness_User_Data",
    "WATCHLIST_DETAILS": "Awareness_Watchlist_Details",
    "SAFE_SCORE_DETAILS": "Awareness_SafeScore_Details",
}
AWARENESS_PERFORMANCE_FUNCTION_NAME = "Awareness Training Performance Details"
AWARENESS_WATCHLIST_FUNCTION_NAME = "Awareness Training Watchlist Details"
AWARENESS_SAFESCORE_FUNCTION_NAME = "Awareness Training SafeScore Details"
AWARENESS_USER_DATA_FUNCTION_NAME = "Awareness Training Phishing User Data"


# *Error Messages for Exception
UNEXPECTED_ERROR_MSG = "Unexpected error : Error-{}."
HTTP_ERROR_MSG = "HTTP error : Error-{}."
REQUEST_ERROR_MSG = "Request error : Error-{}."
CONNECTION_ERROR_MSG = "Connection error : Error-{}."
KEY_ERROR_MSG = "Key error : Error-{}."
TYPE_ERROR_MSG = "Type error : Error-{}."
VALUE_ERROR_MSG = "Value error : Error-{}."
JSON_DECODE_ERROR_MSG = "JSONDecode error : Error-{}."

# *checkpoint related constants
CONN_STRING = os.environ.get("AzureWebJobsStorage", "")
FILE_SHARE_NAME = "awareness-training"
PERFORMANCE_CHECKPOINT_FILE = "performance_details"
PERFORMANCE_HASH_FILE = "performance_details_hash"
WATCHLIST_CHECKPOINT_FILE = "watchlist_details"
WATCHLIST_HASH_FILE = "watchlist_details_hash"
SAFESCORE_CHECKPOINT_FILE = "safescore_details"
SAFESCORE_HASH_FILE = "safescore_details_hash"

# *Extra constants
MAX_RETRIES = 3
