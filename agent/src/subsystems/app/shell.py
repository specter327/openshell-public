# applications/shell.py

from shared.modules.shell.server import (
    ShellServer
)


class ShellApplication:

    def __init__(
        self,
        core,
        communication
    ):

        self.core = core

        self.communication = communication

        #self.session_token = session_token

        self.client = None

    async def start(self):

        runtime = self.core.runtime

        self.client = ShellServer(
            communication_handler=self.communication,
            auth_token=runtime.auth_token,
            tunnel_token=runtime.tunnel_token,
            #session_token=self.session_token
        )

        await self.client.start()

    async def stop(self):

        pass