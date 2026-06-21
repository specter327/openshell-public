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

        await self.shell.start()

        return

        client = OSAMClient(
            host="127.0.0.1",
            port=8000,
            protocol="http"
        )

        manager_uid = await client.identity.get_logical_identity()
        manager_pik = await client.identity.get_cryptographic_identity()
        entity_type = await client.identity.get_entity_type()

        print(f"Manager UID: {manager_uid}")
        print(f"Cryptographic identity: {manager_pik}")
        print(f"Entity type: {entity_type}")

        console_identity_profile = self.core.identity.load()
        console_identity_public = console_identity_profile.get("public")
        console_identity_private = console_identity_profile.get("private")

        console_uid = console_identity_public.get("identification").get("uid")
        console_pik = console_identity_public.get("cryptographic_identity").get("public_key")
        console_ppik = console_identity_private.get("cryptographic_identity").get("private_key")

        print(f"Console UID: {console_uid}")
        print(f"Console PIK: {console_pik}")

        client_authentication = await self.core.manager.client_authenticate()

        print(client_authentication)
        server_authentication = await self.core.manager.server_authenticate()
        print(server_authentication)