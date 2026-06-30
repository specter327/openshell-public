# ==========================================================
# OpenShell Console
# Identity Manager
# ==========================================================

from pathlib import Path

from shared.identity.identification import (
    EntityIdentity
)

from shared.identity.store import (
    IdentityStore
)

from ..service import Subsystem
import fsresource_tree as fs


class IdentityManager(
    Subsystem
):

    def __init__(
        self,
        core
    ):

        super().__init__(core)


    # ======================================================
    # EXISTS
    # ======================================================

    def exists(self):

        return self.store.exists()

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        name="agent"
    ):

        if self.store.exists():

            raise RuntimeError(
                "Identity already exists"
            )

        identity = (
            EntityIdentity.generate(
                name=name
            )
        )

        self.store.save(
            public_profile=(
                identity.export_public()
            ),

            private_profile=(
                identity.to_dict()
            ),

            metadata={
                "type": "agent"
            }
        )

        self.events.publish(
            "identity.created",
            identity
        )

        return identity

    # ======================================================
    # LOAD
    # ======================================================

    def load(self):

        data = self.store.load()

        self.events.publish(
            "identity.loaded",
            data
        )

        return data

    # ======================================================
    # LOAD PUBLIC
    # ======================================================

    def load_public(self):

        return self.store.load_public()

    # ======================================================
    # EXPORT
    # ======================================================

    def export(
        self,
        directory
    ):

        path = self.store.export_public(
            Path(directory)
        )

        self.events.publish(
            "identity.exported",
            str(path)
        )

        return path

    # ======================================================
    # STATUS
    # ======================================================

    def status(self):

        return {
            "available": (
                self.store.exists()
            )
        }

    async def start(self) -> bool:
        self._storage_service = self.services.get("storage")

        self.store = IdentityStore(
            base_path=fs.operations.path(self._storage_service.storage_schema.DATA_ROOT),
            namespace="agent"
        )

        return True

    async def stop(self) -> bool:
        return True