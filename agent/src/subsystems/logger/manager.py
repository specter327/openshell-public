# =========================================================
# OpenShell Logging Service
# =========================================================

from pathlib import Path

from loguru import logger

from ..service import Subsystem
import fsresource_tree as fs


class LoggingService(Subsystem):
    LOG_DIR: fs.File = fs.File(
        name="logs"
    )

    """
    Centralized system logging service.

    Provides a shared interface for all system components
    to write operational logs.

    Backend:
        loguru
    """



    def __init__(
        self,
        core
    ):

        super().__init__(core)

        self.initialized = False

        self.log_directory = None



    # =====================================================
    # LIFECYCLE
    # =====================================================

    async def start(self):
        self._storage_service = self.services.get("storage")

        await self.configure()

        self.initialized = True



    async def stop(self):

        self.initialized = False



    # =====================================================
    # CONFIGURATION
    # =====================================================

    async def configure(self):
        self._storage_service.storage_schema.storage_tree.register(
            resource=self.LOG_DIR,
            parent=self._storage_service.storage_schema.DATA_ROOT
        )

        #self._storage_service.storage_schema.file_system.operations.create(
        #    self.LOG_DIR,
        #    recursive_parent=True,
        #    recursive_children=True
        #)

        logger.remove()
        logger.add(
            fs.operations.path(self.LOG_DIR) + "/{time:DD-MM-YY-HH-mm-ss}.log",
            rotation="10 MB",
            retention=None,
            compression=None,
            enqueue=True,
            encoding="utf-8",
            backtrace=True,
            diagnose=False,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level} | "
                "{extra[source]} | "
                "{message}"
            )
        )


    # =====================================================
    # LOGGING
    # =====================================================

    def log(
        self,
        source,
        message,
        level="INFO",
        **context
    ):

        logger.bind(
            source=source,
            **context
        ).log(
            level,
            message
        )



    def debug(
        self,
        source,
        message,
        **context
    ):

        self.log(
            source,
            message,
            "DEBUG",
            **context
        )



    def info(
        self,
        source,
        message,
        **context
    ):

        self.log(
            source,
            message,
            "INFO",
            **context
        )



    def warning(
        self,
        source,
        message,
        **context
    ):

        self.log(
            source,
            message,
            "WARNING",
            **context
        )



    def error(
        self,
        source,
        message,
        **context
    ):

        self.log(
            source,
            message,
            "ERROR",
            **context
        )



    def critical(
        self,
        source,
        message,
        **context
    ):

        self.log(
            source,
            message,
            "CRITICAL",
            **context
        )