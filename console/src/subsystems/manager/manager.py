# ==========================================================
# OpenShell Console
# Manager Subsystem
# ==========================================================


from ..service import Subsystem
from ...shared.api.manager.v1 import OSAMClient


class ManagerSubsystem(Subsystem):


    def __init__(
        self,
        core
    ):
        super().__init__(
            core
        )

    # ======================================================
    # CLIENT AUTHENTICATION
    # ======================================================
    async def client_authenticate(
        self
    ) -> str:
        """
        Authenticate Console against Manager.

        Console proves ownership of its identity.

        Returns:
            auth_token
        """


        identity = (
            self.core.identity.load()
        )


        public = identity.get(
            "public"
        )

        private = identity.get(
            "private"
        )


        entity_uid = (
            public
            .get("identification")
            .get("uid")
        )


        entity_pik = (
            public
            .get("cryptographic_identity")
            .get("public_key")
        )


        entity_ppik = (
            private
            .get("cryptographic_identity")
            .get("private_key")
        )


        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )


        result = await (
            client.authentication
            .authenticate_client(
                entity_uid=entity_uid,
                entity_pik=entity_pik,
                entity_ppik=entity_ppik
            )
        )


        return result["auth_token"]



    # ======================================================
    # SERVER AUTHENTICATION
    # ======================================================

    async def server_authenticate(
        self
    ) -> bool:
        """
        Authenticate remote Manager.

        Console verifies that Manager owns
        its public identity.

        Returns:
            bool
        """


        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )
        
        manager_identity = await (
            client.identity
            .get_logical_identity()
        )


        manager_crypto = await (
            client.identity
            .get_cryptographic_identity()
        )


        console_identity = (
            self.core.identity.load()
        )


        console_uid = (
            console_identity
            .get("public")
            .get("identification")
            .get("uid")
        )


        result = await (
            client.authentication
            .authenticate_server(
                client_uid=console_uid,

                server_uid=(
                    manager_identity.uid
                ),

                server_public_key=(
                    manager_crypto.public_key
                )
            )
        )


        return result

    # ======================================================
    # CLOSED INTEGRATION
    # ======================================================


    async def closed_integration(
        self,
        security_code: str
    ) -> dict:
        """
        Integrate console using CLOSED passport.

        Requires:
            runtime.auth_token

        Server stores:
            Entity <-> Domain relationship

        Console stores nothing.
        """


        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        if not auth_token:

            raise Exception(
                "Console not authenticated"
            )


        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )


        result = await (
            client.passports
            .integrate_closed(
                auth_token=auth_token,
                security_code=security_code
            )
        )


        return result.to_dict()

    # ==========================================================
    # OPEN PASSPORT CREATION
    # ==========================================================

    async def create_open_passport(
        self,
        domain_uid: str,
        entity_role: str,
        expiration_hours: int = 24,
        usage_limit: int = 1
    ):
        """
        Request OPEN passport creation.

        Requires:
            - authenticated console
            - auth_token

        Manager validates:
            - domain membership
            - console integration
            - permissions

        Returns:
            Passport
        """

        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        if not auth_token:

            raise Exception(
                "Console is not authenticated"
            )


        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )


        passport = await (
            client.passports
            .create_open(
                auth_token=auth_token,

                domain_uid=domain_uid,

                entity_role=entity_role,

                expiration_hours=expiration_hours,

                usage_limit=usage_limit
            )
        )


        return passport

    # ======================================================
    # ENTITY QUERY
    # ======================================================

    async def query_entities(
        self,
        entity_type: str | None = None
    ) -> list[dict]:
        """
        Query visible entities.

        The Manager owns the state.
        Console only requests information.

        Args:
            entity_type:
                Optional entity filter.
                Example:
                    AGENT
                    CONSOLE
                    SERVICE

        Returns:
            List of entities
        """


        auth_token = (
            self.core
            .runtime
            .auth_token
        )


        if not auth_token:

            raise Exception(
                "Console is not authenticated"
            )


        client = OSAMClient(
            host=self.core.runtime.manager_address,
            port=self.core.runtime.manager_port,
            protocol=self.core.runtime.manager_protocol
        )


        entities = await (
            client.entities
            .query(
                auth_token=auth_token,
                entity_type=entity_type
            )
        )

        return entities

    # ======================================================
    # SESSION MANAGEMENT
    # ======================================================

