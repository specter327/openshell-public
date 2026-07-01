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
    ELEMENT_NAME: str = "IDENTITY-MANAGER"

    def __init__(
        self,
        core
    ):

        super().__init__(core)
        self._logger = self.services.get("logger")


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
        self._logger.log(source=self.ELEMENT_NAME, message="Creating an identity profile")

        if self.store.exists():
            self._logger.error(source=self.ELEMENT_NAME, message="Existing identity profile")

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

        self._logger.info(source=self.ELEMENT_NAME, message="Identity profile created and stored")

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

        self._logger.info(source=self.ELEMENT_NAME, message="Identity profile uploaded")

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