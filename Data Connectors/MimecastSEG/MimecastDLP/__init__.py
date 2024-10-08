"""Init file for Mimecast SEG DLP function."""

import datetime
import logging
import time
import azure.functions as func
from .mimecast_dlp_to_sentinel import MimecastDLPToSentinel
from ..SharedCode.logger import applogger
from ..SharedCode import consts


def main(mytimer: func.TimerRequest) -> None:
    """Run the main logic of the Function App triggered by a timer."""
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    start = time.time()
    applogger.info(
        "{} : {}, Function started at {}".format(
            consts.LOGS_STARTS_WITH,
            consts.SEG_DLP_FUNCTION_NAME,
            datetime.datetime.fromtimestamp(start),
        )
    )
    mimecast_to_sentinel_obj = MimecastDLPToSentinel(int(start))
    mimecast_to_sentinel_obj.get_mimecast_dlp_data_in_sentinel()
    end = time.time()

    applogger.info(
        "{} : {}, Function ended at {}".format(
            consts.LOGS_STARTS_WITH,
            consts.SEG_DLP_FUNCTION_NAME,
            datetime.datetime.fromtimestamp(end),
        )
    )
    applogger.info(
        "{} : {}, Total time taken = {}".format(consts.LOGS_STARTS_WITH, consts.SEG_DLP_FUNCTION_NAME, end - start)
    )
    if mytimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function ran at %s", utc_timestamp)
