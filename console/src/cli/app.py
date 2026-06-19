from .context import ConsoleContext
from .router import CommandRouter
from .shell import ConsoleShell


from .commands.manager import register as manager
from .commands.identity import register as identity
from .commands.domains import register as domains
from .commands.sessions import register as sessions
from .commands.tunnels import register as tunnels
from .commands.support import register as support
from .commands.help import register as rhelp


class ConsoleApplication:


    def __init__(self):

        self.context=ConsoleContext()

        self.router=CommandRouter()


        manager(self.router)
        identity(self.router)
        domains(self.router)
        sessions(self.router)
        tunnels(self.router)
        support(self.router)
        rhelp(self.router)



    async def start(self):

        shell=ConsoleShell(
            self.context,
            self.router
        )


        await shell.start()