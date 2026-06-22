# ==========================================================
# OpenShell Console
# Base Subsystem
# ==========================================================


class Subsystem:

    def __init__(
        self,
        core
    ):

        self.core = core

        self.events = core.events

        self.services = core.services

        self.runtime = core.runtime