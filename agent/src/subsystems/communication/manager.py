# ==========================================================
# OpenShell Console
# Communication Subsystem
# ==========================================================

from ..service import Subsystem

from ...shared.modules.utils import (
    CommunicationHandler
)


class CommunicationSubsystem(
    Subsystem
):


    def __init__(
        self,
        core
    ):
        super().__init__(
            core
        )

        self.handler = None
        self.connected = False


    # ======================================================
    # CONNECT
    # ======================================================

    async def connect(
        self
    ) -> bool:
        """
        Connect to the authorized tunnel.

        Requirements:
            - authenticated console
            - authorized tunnel

        Creates:
            CommunicationHandler

        Returns:
            bool
        """

        runtime = (
            self.core.runtime
        )


        if not runtime.authenticated:

            raise Exception(
                "Console is not authenticated"
            )


        if not runtime.tunnel_authorized:

            raise Exception(
                "Tunnel is not authorized"
            )


        if self.connected:

            return True


        self.handler = (
            CommunicationHandler(
                auth_token=(
                    runtime.auth_token
                ),

                tunnel_token=(
                    runtime.tunnel_token
                ),

                tunnel_host=(
                    runtime.tunnel_host
                ),

                tunnel_port=(
                    runtime.tunnel_port
                )
            )
        )


        await self.handler.connect()


        self.connected = True


        if hasattr(
            runtime,
            "communication_connected"
        ):
            runtime.communication_connected = True


        return True


    # ======================================================
    # SEND
    # ======================================================

    async def send(
        self,
        packet: dict
    ) -> bool:
        """
        Send datapackage.

        Args:
            packet

        Returns:
            bool
        """

        if not self.connected:

            raise Exception(
                "Communication is not connected"
            )


        await (
            self.handler
            .send_datapackage(
                packet
            )
        )

        return True


    # ======================================================
    # RECEIVE
    # ======================================================

    async def receive(
        self
    ) -> dict:
        """
        Receive datapackage.

        Returns:
            dict
        """

        if not self.connected:

            raise Exception(
                "Communication is not connected"
            )


        return await (
            self.handler
            .receive_datapackage()
        )


    # ======================================================
    # STATUS
    # ======================================================

    def status(
        self
    ) -> dict:

        runtime = (
            self.core.runtime
        )


        return {

            "connected":
                self.connected,

            "authenticated":
                runtime.authenticated,

            "tunnel_authorized":
                runtime.tunnel_authorized,

            "tunnel_host":
                runtime.tunnel_host,

            "tunnel_port":
                runtime.tunnel_port
        }


    # ======================================================
    # CLOSE
    # ======================================================

    async def close(
        self
    ) -> bool:
        """
        Close communication channel.

        Returns:
            bool
        """

        if self.handler:

            try:

                await (
                    self.handler
                    .close()
                )

            finally:

                self.handler = None


        self.connected = False


        if hasattr(
            self.core.runtime,
            "communication_connected"
        ):
            self.core.runtime.communication_connected = False


        return True


    # ======================================================
    # RECONNECT
    # ======================================================

    async def reconnect(
        self
    ) -> bool:
        """
        Reconnect communication channel.
        """

        await self.close()

        return await self.connect()

    # ======================================================
    # COMPATIBILITY LAYER
    # ======================================================

    async def send_datapackage(
        self,
        packet: dict
    ):
        return await self.send(
            packet
        )


    async def receive_datapackage(
        self
    ):
        return await self.receive()