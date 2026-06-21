# ==========================================================
# OpenShell Console
# Domain Subsystem
# ==========================================================
from ...shared.api.manager.v1 import OSAMClient


class DomainManager:


    def __init__(
        self,
        core
    ):

        self.core = core

        self.events = core.events
        self.services = core.services



    # ======================================================
    # QUERY DOMAINS
    #
    # STATE-LESS
    #
    # Uses:
    # runtime.auth_token
    #
    # ======================================================


    async def query(self):


        runtime = (
            self.core.runtime
        )


        if not runtime.authenticated:

            raise Exception(
                "Console not authenticated"
            )


        auth_token = (
            runtime.auth_token
        )


        client = OSAMClient(
            host=runtime.manager_address,
            port=runtime.manager_port,
            protocol=runtime.manager_protocol
        )


        domains = await (
            client.domains.query(
                auth_token
            )
        )


        return domains