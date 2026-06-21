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

        self.identity = IdentityManager(
            self
        )

        self.manager = ManagerSubsystem(
            self
        )

        self.domain = DomainManager(
            self
        )

        self.tunnel = TunnelManager(
            self
        )

        self.session = SessionManager(
            self
        )

        self.app = AppManager(
            self
        )

        self.communication = CommunicationSubsystem(
            self
        )

        # --------------------------------------------------
        # Registry
        # --------------------------------------------------

        self.services.register(
            "identity",
            self.identity
        )

        self.services.register(
            "manager",
            self.manager
        )

        self.services.register(
            "domain",
            self.domain
        )

        self.services.register(
            "tunnel",
            self.tunnel
        )

        self.services.register(
            "session",
            self.session
        )

        self.services.register(
            "app",
            self.app
        )

        self.app.register(
            "shell",
            ShellApplication
        )

        self.services.register(
            "communication",
            self.communication
        )