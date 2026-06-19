#!/usr/bin/env python3

# ==========================================================
# OpenShell Global Event Logger
# ==========================================================


import os
import logging

from datetime import datetime
from logging.handlers import RotatingFileHandler



# ==========================================================
# PATH
# ==========================================================


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)


os.makedirs(
    LOG_DIR,
    exist_ok=True
)



LOG_FILE = os.path.join(
    LOG_DIR,
    "console.log"
)



# ==========================================================
# CUSTOM ROTATION
# ==========================================================


class TimestampRotatingHandler(
    RotatingFileHandler
):


    def doRollover(self):

        if self.stream:

            self.stream.close()
            self.stream = None


        if os.path.exists(
            self.baseFilename
        ):

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )


            directory = os.path.dirname(
                self.baseFilename
            )


            filename = os.path.basename(
                self.baseFilename
            )


            name, ext = os.path.splitext(
                filename
            )


            rotated = os.path.join(
                directory,
                f"{name}_{timestamp}{ext}"
            )


            os.rename(
                self.baseFilename,
                rotated
            )


        if not self.delay:

            self.stream = self._open()



# ==========================================================
# LOGGER CREATION
# ==========================================================


def create_logger():

    logger = logging.getLogger(
        "OpenShell"
    )


    if logger.handlers:

        return logger



    logger.setLevel(
        logging.DEBUG
    )


    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s "
            "[%(levelname)s] "
            "[%(module)s] "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )



    handler = TimestampRotatingHandler(

        LOG_FILE,

        maxBytes=
            10 * 1024 * 1024,

        backupCount=
            100,

        encoding="utf-8"

    )


    handler.setFormatter(
        formatter
    )


    logger.addHandler(
        handler
    )


    # consola también

    console = logging.StreamHandler()

    console.setFormatter(
        formatter
    )


    logger.addHandler(
        console
    )


    return logger



# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


logger = create_logger()