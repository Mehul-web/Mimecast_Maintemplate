"""Get Mimecast Awareness Training Watchlist data and ingest into sentinel."""

import inspect
from ..SharedCode import consts
from ..SharedCode.mimecast_exception import MimecastException, MimecastTimeoutException
from ..SharedCode.logger import applogger
from ..SharedCode.state_manager import StateManager
from ..SharedCode.utils import Utils
import time


class MimecastAwarenessWatchlist(Utils):
    """Class for Mimecast Awareness Training Watchlist Details."""

    def __init__(self, start_time) -> None:
        """Initialize utility methods and variables.

        Args:
            start_time (str): azure function starting time.
        """
        super().__init__(consts.AWARENESS_WATCHLIST_FUNCTION_NAME)
        self.check_environment_var_exist(
            [
                {"BaseURL": consts.BASE_URL},
                {"WorkspaceID": consts.WORKSPACE_ID},
                {"WorkspaceKey": consts.WORKSPACE_KEY},
                {"MimecastClientID": consts.MIMECAST_CLIENT_ID},
                {"MimecastClientSecret": consts.MIMECAST_CLIENT_SECRET},
                {"ConnectionString": consts.CONN_STRING},
                {"LogLevel": consts.LOG_LEVEL},
            ]
        )
        self.authenticate_mimecast_api()
        self.state_manager_obj = StateManager(
            consts.CONN_STRING, consts.WATCHLIST_CHECKPOINT_FILE, consts.FILE_SHARE_NAME
        )
        self.hash_file_state_manager_obj = StateManager(
            consts.CONN_STRING, consts.WATCHLIST_HASH_FILE, consts.FILE_SHARE_NAME
        )
        self.watchlist_details_url = consts.BASE_URL + consts.ENDPOINTS["WATCHLIST_DETAILS"]
        self.function_start_time = start_time

    def get_request_body(self):
        """Get request body with page token if available in checkpoint.

        Returns:
            dict: request body
        """
        __method_name = inspect.currentframe().f_code.co_name
        try:
            request_body = {"meta": {"pagination": {"pageSize": consts.MAX_PAGE_SIZE}}}
            checkpoint = self.get_checkpoint_data(self.state_manager_obj, False)
            if checkpoint:
                applogger.info(
                    self.log_format.format(
                        consts.LOGS_STARTS_WITH,
                        __method_name,
                        self.azure_function_name,
                        "Page checkpoint found.",
                    )
                )
                request_body["meta"]["pagination"]["pageToken"] = checkpoint
                applogger.debug(
                    self.log_format.format(
                        consts.LOGS_STARTS_WITH,
                        __method_name,
                        self.azure_function_name,
                        "Page checkpoint data : {}.".format(checkpoint),
                    )
                )
            else:
                applogger.info(
                    self.log_format.format(
                        consts.LOGS_STARTS_WITH, __method_name, self.azure_function_name, "Page checkpoint not found."
                    )
                )
            return request_body
        except MimecastException:
            raise MimecastException()
        except Exception as err:
            applogger.error(
                self.log_format.format(
                    consts.LOGS_STARTS_WITH,
                    __method_name,
                    self.azure_function_name,
                    consts.UNEXPECTED_ERROR_MSG.format(err),
                )
            )
            raise MimecastException()

    def get_awareness_watchlist_details_data_in_sentinel(self):
        """Get Mimecast awareness training watchlist details data and ingest to sentinel."""
        __method_name = inspect.currentframe().f_code.co_name
        try:
            request_body = self.get_request_body()
            next_page = True
            while next_page:
                if int(time.time()) >= self.function_start_time + consts.FUNCTION_APP_TIMEOUT_SECONDS:
                    raise MimecastTimeoutException()
                watchlist_details_response = self.make_rest_call(
                    method="POST", url=self.watchlist_details_url, json=request_body
                )
                watchlist_details_data = watchlist_details_response["data"]
                if len(watchlist_details_data) > 0:
                    self.filter_unique_data_and_post(
                        watchlist_details_data, self.hash_file_state_manager_obj, consts.TABLE_NAME["WATCHLIST_DETAILS"]
                    )
                    next_page_token = watchlist_details_response["meta"]["pagination"].get("next", "")
                    if next_page_token:
                        request_body["meta"]["pagination"]["pageToken"] = next_page_token
                        applogger.debug(
                            self.log_format.format(
                                consts.LOGS_STARTS_WITH,
                                __method_name,
                                self.azure_function_name,
                                "Posting page checkpoint : {}.".format(next_page_token),
                            )
                        )
                        self.post_checkpoint_data(self.state_manager_obj, next_page_token, False)
                    else:
                        next_page = False
                        hash_data_to_save = self.convert_to_hash(watchlist_details_data)
                        applogger.info(
                            self.log_format.format(
                                consts.LOGS_STARTS_WITH,
                                __method_name,
                                self.azure_function_name,
                                "Posting hash checkpoint.",
                            )
                        )
                        self.post_checkpoint_data(self.hash_file_state_manager_obj, hash_data_to_save, True)
                        applogger.info(
                            self.log_format.format(
                                consts.LOGS_STARTS_WITH, __method_name, self.azure_function_name, "End of data."
                            )
                        )
                else:
                    next_page = False
                    applogger.info(
                        self.log_format.format(
                            consts.LOGS_STARTS_WITH, __method_name, self.azure_function_name, "No data found."
                        )
                    )
        except KeyError as key_error:
            applogger.error(
                self.log_format.format(
                    consts.LOGS_STARTS_WITH,
                    __method_name,
                    self.azure_function_name,
                    consts.KEY_ERROR_MSG.format(key_error),
                )
            )
            raise MimecastException()
        except MimecastTimeoutException:
            applogger.info(
                self.log_format.format(
                    consts.LOGS_STARTS_WITH,
                    __method_name,
                    self.azure_function_name,
                    "function app 9:30 mins executed hence breaking.",
                )
            )
            return
        except MimecastException:
            raise MimecastException()
        except Exception as err:
            applogger.error(
                self.log_format.format(
                    consts.LOGS_STARTS_WITH,
                    __method_name,
                    self.azure_function_name,
                    consts.UNEXPECTED_ERROR_MSG.format(err),
                )
            )
            raise MimecastException()
