# ==========================================================
# OpenShell Console
# Tunnel Manager Subsystem
# ==========================================================


from ..service import Subsystem
from shared.api.manager.v1 import OSAMClient


class TunnelManager(Subsystem):
    """
    Tunnel management subsystem.

    Responsibilities:
        - Request communication tunnel
        - Store tunnel runtime state
        - Expose tunnel information

    Does NOT:
        - Perform HTTP directly
        - Open sockets
        - Create sessions
        - Handle shell communication
    """



    # ======================================================
    # TUNNEL REQUEST
    # ======================================================

    async def request_tunnel(
        self
    ) -> dict:
        """
        Request communication tunnel.

        Flow:

            Console
              |
              v
            TunnelManager
              |
              v
            OSAMClient
              |
              v
            TunnelsAPI.request()
              |
              v
            Manager Server


        Requires:

            runtime.authenticated == True


        Stores:

            runtime.tunnel_token
            runtime.tunnel_host
            runtime.tunnel_port


        Returns:

            Tunnel information dictionary
        """


        #
        # Validate authentication state
        #

        if not self.runtime.authenticated:

            raise RuntimeError(
                "Console is not authenticated"
            )



        if not self.runtime.auth_token:

            raise RuntimeError(
                "Missing authentication token"
            )



        #
        # Use SDK client
        #

        client = OSAMClient(
            host=self.runtime.manager_address,
            port=self.runtime.manager_port,
            protocol=self.runtime.manager_protocol
        )

        tunnel_response = await client.tunnels.request(
            auth_token=self.runtime.auth_token
        )

        print(tunnel_response)


        #
        # Validate server response
        #

        if not tunnel_response:

            raise RuntimeError(
                "Empty tunnel response"
            )



        tunnel_token = (
            tunnel_response
            .get("tunnel_token")
        )


        if not tunnel_token:

            raise RuntimeError(
                "Tunnel authorization failed"
            )



        #
        # Store runtime state
        #

        self.runtime.set_tunnel(

            tunnel_token=tunnel_token,

            tunnel_host=(
                self.runtime.manager_address
            ),

            tunnel_port=(
                tunnel_response
                .get("tunnel_port")
            )
        )



        return tunnel_response



    # ======================================================
    # TUNNEL STATUS
    # ======================================================

    def status(
        self
    ) -> dict:
        """
        Return current tunnel runtime state.
        """


        return {

            "authorized":
                self.runtime.tunnel_authorized,


            "token":
                self.runtime.tunnel_token,


            "host":
                self.runtime.tunnel_host,


            "port":
                self.runtime.tunnel_port
        }



    # ======================================================
    # TUNNEL CLEAR
    # ======================================================

    def clear(
        self
    ) -> bool:
        """
        Remove current tunnel state.
        """


        self.runtime.clear_tunnel()


        return True