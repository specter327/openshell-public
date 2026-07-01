from .context import ConsoleContext
from .router import CommandRouter
from .shell import ConsoleShell
from ..core import ConsoleCore


from .commands.manager import register as manager
from .commands.identity import register as identity
from .commands.domains import register as domains
from .commands.sessions import register as sessions
from .commands.tunnels import register as tunnels
from .commands.support import register as support
from .commands.help import register as rhelp
from .commands.authentication import register as authentication
from .commands.integration import register as integration
from .commands.passports import register as passports
from .commands.entities import register as entities
from .commands.shell import register as shell
from .commands.communication import register as communication

class ConsoleApplication:


    def __init__(self):
        self.core = ConsoleCore()
        self.context = ConsoleContext(
            self.core
        )
        self.router = CommandRouter()
        self.shell = ConsoleShell(
            self.context,
            self.router
        )


    async def start(self):
        print(f"Core: {self.core}")
        identity_service = self.core.services.get("identity")

        # Verify Console existence
        if not identity_service.exists():
            print(f"[*] Creating Console identity...")
            print(f"[#] Type your Console name:")
            identity_service.create(input(">>> "))

        # Load Console identity
        console_identity = identity_service.load()

        # Save Console identity on the runtime
        self.core.runtime.set_console_profile(console_identity)
        self.core.runtime.set_manager_address("www.fortaprest.org")
        self.core.runtime.set_manager_port(443)
        self.core.runtime.set_manager_protocol("https")
        manager(self.router)
        identity(self.router)
        domains(self.router)
        sessions(self.router)
        tunnels(self.router)
        support(self.router)
        rhelp(self.router)
        authentication(self.router)
        integration(self.router)
        passports(self.router)
        entities(self.router)
        shell(self.router)
        communication(self.router)

        await self.shell.start()