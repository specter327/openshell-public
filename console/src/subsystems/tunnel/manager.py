# manager/subsystems/tunnel.py

from shared.osam.tunnels import TunnelsAPI
from ..service import Subsystem

class TunnelManager(Subsystem):
    """
    Gestión del ciclo de vida del túnel.

    Responsabilidades:
    - Solicitar túnel
    - Guardar estado en runtime
    - Exponer información del túnel

    No:
    - abrir sockets
    - crear sesiones
    - ejecutar shell
    """
    async def request(self):

        if not self.runtime.authenticated:
            raise RuntimeError(
                "Authentication required"
            )


        tunnel = await self.client.tunnels.request(
            auth_token=self.runtime.auth_token
        )


        if not tunnel.tunnel_token:
            raise RuntimeError(
                "Tunnel request failed"
            )


        self.runtime.set_tunnel(
            tunnel_token=tunnel.tunnel_token,
            tunnel_host=tunnel.host,
            tunnel_port=tunnel.port
        )


        return tunnel


    def status(self):

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