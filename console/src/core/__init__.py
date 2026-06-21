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
from src.subsystems.domain import (
    DomainManager
)

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
