# Library import
from pathlib import Path
from typing import Optional
import shutil

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
    # SOURCE
    # =====================================================

    def bootstrap_path(self) -> Path:
        """
        Bootstrap package bundled with the executable.
        """

        return (
            self.environment.bundle_root
            / self.BOOTSTRAP_ROOT.name
        )

    # =====================================================
    # DESTINATION
    # =====================================================

    def destination_path(self) -> Path:
        """
        Persistent bootstrap location.
        """

        return Path(
            self._storage_service
            .storage_schema
            .file_system
            .operations
            .path(self.BOOTSTRAP_ROOT)
        )

    # =====================================================
    # STATUS
    # =====================================================

    async def exists(self) -> bool:

        return self.bootstrap_path().exists()

    # =====================================================
    # INSTALL
    # =====================================================

    async def install(self) -> Path:
        """
        Copy bundled bootstrap resources into the
        persistent storage location.
        """

        source = self.bootstrap_path()
        destination = self.destination_path()

        if destination.exists():

            print(
                "[BOOTSTRAP] Bootstrap already installed."
            )

            return destination

        print(
            f"[BOOTSTRAP] Installing bootstrap package..."
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copytree(
            src=source,
            dst=destination,
            dirs_exist_ok=True
        )

        print(
            f"[BOOTSTRAP] Bootstrap installed: {destination}"
        )

        return destination

    # =====================================================
    # LOAD
    # =====================================================

    async def load(self) -> fs.Directory:

        #
        # Register root
        #

        if not self.resource_tree.registered(
            self.BOOTSTRAP_ROOT
        ):

            self.resource_tree.register(
                resource=self.BOOTSTRAP_ROOT
            )

        #
        # Ensure bootstrap is installed
        #

        root_path = await self.install()

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

            resource = fs.File(
                name=child.stem,
                extension=child.suffix.lstrip(".")
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

        for resource in self.resource_tree.resources.values():

            if resource.name == name:

                return resource

        return None

    # =====================================================
    # START
    # =====================================================

    async def start(self) -> bool:

        self._storage_service = self.services.get(
            "storage"
        )

        self.resource_tree = (
            self._storage_service
            .storage_schema
            .storage_tree
        )

        #
        # Register bootstrap root
        #

        if not self.resource_tree.registered(
            self.BOOTSTRAP_ROOT
        ):

            self.resource_tree.register(
                resource=self.BOOTSTRAP_ROOT,
                parent=self._storage_service
                .storage_schema
                .AGENT_ROOT
            )

        print(
            f"[BOOTSTRAP] Bundle root: "
            f"{self.environment.bundle_root}"
        )

        print(
            f"[BOOTSTRAP] Bundle bootstrap: "
            f"{self.bootstrap_path()}"
        )

        print(
            f"[BOOTSTRAP] Storage bootstrap: "
            f"{self.destination_path()}"
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
                self._storage_service
                .storage_schema
                .AGENT_ROOT
            )
        )

        return True

    # =====================================================
    # STOP
    # =====================================================

    async def stop(self) -> bool:

        return True