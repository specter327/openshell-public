# ==========================================================
# OpenShell Console Context
# ==========================================================


from pathlib import Path

from shared.identity.store import IdentityStore
from .output import ConsoleOutput


class ConsoleContext:

    def __init__(
        self,
        core
    ):
        self.core = core

        self.output = ConsoleOutput(
            enable_colors=True
        )