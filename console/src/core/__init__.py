# ==========================================================
# OpenShell Console
# Core
# ==========================================================

from .events import EventManager
from .registry import ServiceRegistry

from src.subsystems.identity import (
    IdentityManager
)

from src.subsystems.manager import ManagerSubsystem
from src.subsystems.domain import DomainManager
from src.subsystems.tunnel import TunnelManager
from src.subsystems.session import SessionManager
from src.subsystems.app import AppManager
from src.subsystems.communication import CommunicationSubsystem
from src.subsystems.app.shell import ShellApplication
from src.subsystems.storage import StorageManager
from src.subsystems.settings import SettingsManager


from .runtime import CoreRuntime


class ConsoleCore:

    def __init__(self):

        # --------------------------------------------------
        # Infrastructure
        # --------------------------------------------------

        self.events = EventManager()

        self.services = ServiceRegistry()

        self.runtime = CoreRuntime()

        # --------------------------------------------------
        # Subsystems
        # --------------------------------------------------
        self.storage = StorageManager(self); self.services.register("storage", self.storage)
        self.setting = SettingsManager(self); self.services.register("setting", self.setting)
        self.identity = IdentityManager(self); self.services.register("identity", self.identity)
        self.manager = ManagerSubsystem(self); self.services.register("manager", self.manager)
        self.domain = DomainManager(self); self.services.register("domain", self.domain)
        self.tunnel = TunnelManager(self); self.services.register("tunnel", self.tunnel)
        self.session = SessionManager(self); self.services.register("session", self.session)

        self.app = AppManager(self); self.services.register("app", self.app)
        self.app.register("shell", ShellApplication)
        self.communication = CommunicationSubsystem(self); self.services.register("communication", self.communication)

    async def start(self) -> bool:
        # Start services
        await self.storage.start()
        # self.bootstrap.start()
        await self.identity.start()
        # self.install.install()
        await self.communication.start()
        await self.setting.start()

        return True

    async def stop(self) -> bool:
        return True