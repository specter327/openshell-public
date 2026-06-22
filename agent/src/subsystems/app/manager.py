# ==========================================================
# OpenShell Console
# Application Manager
# ==========================================================

import asyncio

from ..service import Subsystem


class AppManager(Subsystem):
    """
    Application lifecycle manager.

    Responsibilities:
        - Register applications
        - Start applications
        - Stop applications
        - Provide exclusive access to communication layer

    Applications do not access the transport directly.

    Instead:

        app_manager.run("shell")

    acquires the communication lock and
    injects CommunicationManager.
    """

    def __init__(
        self,
        core
    ):
        super().__init__(core)

        self._applications = {}

        self._active_name = None
        self._active_instance = None

        self._communication_lock = asyncio.Lock()

    # ======================================================
    # REGISTRATION
    # ======================================================

    def register(
        self,
        name: str,
        application_cls
    ) -> bool:

        self._applications[name] = application_cls

        return True

    # ======================================================
    # QUERY
    # ======================================================

    def registered(self) -> list:

        return list(
            self._applications.keys()
        )

    def exists(
        self,
        name: str
    ) -> bool:

        return (
            name in self._applications
        )

    # ======================================================
    # ACTIVE APP
    # ======================================================

    @property
    def active(self):

        return self._active_name

    @property
    def active_instance(self):

        return self._active_instance

    # ======================================================
    # RUN
    # ======================================================

    async def run(
        self,
        name: str,
        **kwargs
    ):
        """
        Execute application.

        Example:

            await app.run(
                "shell",
                session_token=...
            )
        """

        if name not in self._applications:

            raise Exception(
                f"Unknown application: {name}"
            )

        communication = (
            self.core.services
            .get("communication")
        )

        application_cls = (
            self._applications[name]
        )

        async with self._communication_lock:

            instance = application_cls(
                core=self.core,
                communication=communication,
                **kwargs
            )

            self._active_name = name
            self._active_instance = instance

            try:

                result = await (
                    instance.start()
                )

                return result

            finally:

                self._active_name = None
                self._active_instance = None

    # ======================================================
    # STOP
    # ======================================================

    async def stop(self):

        if not self._active_instance:
            return

        stop_method = getattr(
            self._active_instance,
            "stop",
            None
        )

        if stop_method:

            await stop_method()

        self._active_name = None
        self._active_instance = None

    # ======================================================
    # STATUS
    # ======================================================

    def status(self) -> dict:

        return {

            "active":
                self._active_name,

            "registered":
                self.registered(),

            "locked":
                self._communication_lock.locked()
        }