# ==========================================================
# OpenShell Console
# Session Subsystem Manager
# ==========================================================


from ..service import Subsystem
from ...shared.api.manager.v1 import OSAMClient



class SessionManager(Subsystem):
    """
    Gestión del ciclo de vida de sesiones.

    Responsabilidades:
    - Crear sesiones
    - Listar sesiones activas
    - Cerrar sesiones
    - Guardar sesión activa en runtime

    No:
    - abrir sockets
    - ejecutar shell
    - manejar transporte
    """


    def __init__(
        self,
        core
    ):

        super().__init__(
            core
        )


    # ======================================================
    # CREATE SESSION
    # ======================================================

    async def create(
        self,
        destination_uid: str
    ) -> dict:
        """
        Creates a shell session.

        Requires:

            - authentication
            - active tunnel

        Runtime stores:

            - session_token
            - session_uid
            - source_uid
            - destination_uid
        """


        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        if not auth_token:

            raise Exception(
                "Console is not authenticated"
            )



        tunnel_token = (
            self.core
            .runtime
            .tunnel_token
        )


        if not tunnel_token:

            raise Exception(
                "Tunnel is not available"
            )



        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )



        session = await (
            client.sessions
            .create(
                auth_token=auth_token,

                tunnel_token=tunnel_token,

                destination_uid=destination_uid
            )
        )


        if not session:

            raise Exception(
                "Session creation failed"
            )


        session_token = (
            session.get(
                "session_token"
            )
        )


        if not session_token:

            raise Exception(
                "Invalid session response"
            )


        self.core.runtime.set_session(

            session_uid=(
                session.get(
                    "session_uid"
                )
            ),

            session_token=session_token,

            source_uid=(
                session.get(
                    "source_uid"
                )
            ),

            destination_uid=(
                session.get(
                    "destination_uid"
                )
            )
        )


        return session



    # ======================================================
    # LIST SESSIONS
    # ======================================================


    async def list(
        self
    ) -> list:
        """
        Query active sessions.

        Requires:

            - authentication
            - tunnel
        """


        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        tunnel_token = (
            self.core
            .runtime
            .tunnel_token
        )



        if not auth_token:

            raise Exception(
                "Console is not authenticated"
            )


        if not tunnel_token:

            raise Exception(
                "Tunnel is not available"
            )



        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )



        sessions = await (
            client.sessions
            .list(
                auth_token=auth_token,

                tunnel_token=tunnel_token
            )
        )


        return sessions



    # ======================================================
    # CLOSE SESSION
    # ======================================================


    async def close(
        self,
        session_token: str | None = None
    ) -> dict:
        """
        Close a session.

        If session_token is not supplied,
        closes current runtime session.
        """


        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        tunnel_token = (
            self.core
            .runtime
            .tunnel_token
        )


        if not auth_token:

            raise Exception(
                "Console is not authenticated"
            )


        if not tunnel_token:

            raise Exception(
                "Tunnel is not available"
            )



        if not session_token:

            session_token = (
                self.core
                .runtime
                .session_token
            )



        if not session_token:

            raise Exception(
                "No active session"
            )



        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )



        result = await (
            client.sessions
            .close(
                auth_token=auth_token,

                tunnel_token=tunnel_token,

                session_token=session_token
            )
        )



        #
        # Clear runtime only if
        # closing current session
        #

        if (
            session_token ==
            self.core.runtime.session_token
        ):

            self.core.runtime.clear_session()



        return result



    # ======================================================
    # STATUS
    # ======================================================


    def status(
        self
    ) -> dict:
        """
        Current runtime session state.
        """


        runtime = (
            self.core.runtime
        )


        return {

            "active":
                runtime.session_active,


            "session_uid":
                runtime.session_uid,


            "session_token":
                runtime.session_token,


            "source_uid":
                runtime.source_uid,


            "destination_uid":
                runtime.destination_uid
        }