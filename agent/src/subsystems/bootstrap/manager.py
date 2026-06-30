# Library import
from pathlib import Path
from typing import Optional
import sys

import fsresource_tree as fs

from ..service import Subsystem


# =========================================================
# BOOTSTRAP SERVICE
# =========================================================

class BootstrapService(Subsystem):

    BOOTSTRAP_ROOT = fs.Directory(
        name="bootstrap"
    )

    def __init__(self, core):
        super().__init__(core)

    # =====================================================
    # LOCATION
    # =====================================================


    # =====================================================
    # PATH
    # =====================================================

    def bootstrap_path(self) -> Path:

        return (
            self.environment.bundle_root
            / self.BOOTSTRAP_ROOT.name
        )

    # =====================================================
    # STATUS
    # =====================================================

    async def exists(self) -> bool:

        return self.bootstrap_path().exists()

    # =====================================================
    # LOAD
    # =====================================================

    async def load(self) -> fs.Directory:

        #
        # Already loaded
        #

        if not self.resource_tree.registered(
            self.BOOTSTRAP_ROOT
        ):
            self.resource_tree.register(
                resource=self.BOOTSTRAP_ROOT
            )

        #
        # Register root
        #


        root_path = self.bootstrap_path()

        if not root_path.exists():
            return self.BOOTSTRAP_ROOT

        #
        # Recursive discovery
        #

        self._discover(
            directory=root_path,
            parent=self.BOOTSTRAP_ROOT
        )

        return self.BOOTSTRAP_ROOT

    # =====================================================
    # DISCOVERY
    # =====================================================

    def _discover(
        self,
        directory: Path,
        parent: fs.Directory
    ) -> None:

        for child in directory.iterdir():

            #
            # Directory
            #

            if child.is_dir():

                resource = fs.Directory(
                    name=child.name
                )

                self.resource_tree.register(
                    resource=resource,
                    parent=parent
                )

                self._discover(
                    directory=child,
                    parent=resource
                )

                continue

            #
            # File
            #

            suffix = child.suffix.lstrip(".")

            resource = fs.File(
                name=child.stem,
                extension=suffix
            )

            self.resource_tree.register(
                resource=resource,
                parent=parent
            )

    # =====================================================
    # QUERY
    # =====================================================

    async def get(
        self,
        name: str
    ) -> Optional[fs.Resource]:

        await self.load()

        for resource in self.resource_tree.resources():

            if resource.name == name:
                return resource

        return None

    # =====================================================
    # START
    # =====================================================

    async def start(self) -> bool:

        self._storage_service = self.services.get("storage")
        self.resource_tree = self._storage_service.storage_schema.storage_tree
        self.resource_tree.register(
            self.BOOTSTRAP_ROOT, 
            parent=self._storage_service.storage_schema.AGENT_ROOT
        )


        print(
            f"[BOOTSTRAP] Bundle root: {self.environment.bundle_root}"
        )

        print(
            f"[BOOTSTRAP] Bootstrap path: {self.bootstrap_path()}"
        )

        if not await self.exists():

            print(
                "[BOOTSTRAP] Bootstrap package not found."
            )

            return False

        await self.load()

        print(
            "[BOOTSTRAP] Bootstrap package loaded."
        )

        print(
            fs.renderers.mermaid(
                self._storage_service.storage_schema.AGENT_ROOT
            )
        )

        return True

    # =====================================================
    # STOP
    # =====================================================

    async def stop(self) -> bool:

        return True