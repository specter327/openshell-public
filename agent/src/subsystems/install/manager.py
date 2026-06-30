# Library import
from pathlib import Path
import shutil
import sys

import fsresource_tree as fs

from ..service import Subsystem


class InstallationManager(Subsystem):

    INSTALL_FLAG = fs.File(
        name="installed",
        extension="flag"
    )

    # =====================================================
    # PROGRAM
    # =====================================================
    def get_program_resource(self) -> fs.File:

        return fs.File(
            name="agent"
        )

    # =====================================================
    # INSTALL
    # =====================================================

    async def install(self) -> fs.File:

        storage_service = self.core.services.get("storage")

        if await self.is_installed():
            return self.get_program_resource()

        storage_tree = storage_service.storage_schema.storage_tree
        file_system = storage_service.storage_schema.file_system

        #
        # Register executable
        #

        program = self.get_program_resource()

        if not storage_tree.registered(program):

            storage_tree.register(
                resource=program,
                parent=storage_service.storage_schema.SOFTWARE_ROOT
            )

        #
        # Create executable parent directories
        #

        file_system.operations.create(
            resource=program,
            recursive_parent=True
        )

        #
        # Copy executable
        #

        shutil.copy2(
            self.environment.executable,
            file_system.operations.path(program)
        )

        print(
            f"[INSTALL-MANAGER] Program installed: "
            f"{file_system.operations.path(program)}"
        )

        #
        # Register install flag
        #

        if not storage_tree.registered(self.INSTALL_FLAG):

            storage_tree.register(
                resource=self.INSTALL_FLAG,
                parent=storage_service.storage_schema.DATA_ROOT
            )

        #
        # Create install flag
        #

        file_system.operations.create(
            resource=self.INSTALL_FLAG,
            recursive_parent=True
        )

        print("[INSTALL-MANAGER] Installation completed")

        print(
            file_system.renderers.mermaid(
                storage_service.storage_schema.UNIT_ROOT
            )
        )

        return program

    # =====================================================
    # UNINSTALL
    # =====================================================

    async def uninstall(self) -> bool:

        storage_service = self.core.services.get("storage")

        print(
            "[INSTALL-MANAGER] Deleting: "
            f"{storage_service.storage_schema.file_system.operations.path(storage_service.storage_schema.AGENT_ROOT)}..."
        )

        storage_service.storage_schema.file_system.operations.delete(
            resource=storage_service.storage_schema.AGENT_ROOT,
            recursive_children=True,
            purge=True
        )

        print("[INSTALL-MANAGER] Directory successfully deleted")

        return True

    # =====================================================
    # STATUS
    # =====================================================

    async def is_installed(self) -> bool:

        storage_service = self.core.services.get("storage")

        storage_tree = storage_service.storage_schema.storage_tree
        file_system = storage_service.storage_schema.file_system

        #
        # Register resources (if necessary)
        #

        program = self.get_program_resource()

        if not storage_tree.registered(program):

            storage_tree.register(
                resource=program,
                parent=storage_service.storage_schema.SOFTWARE_ROOT
            )

        if not storage_tree.registered(self.INSTALL_FLAG):

            storage_tree.register(
                resource=self.INSTALL_FLAG,
                parent=storage_service.storage_schema.DATA_ROOT
            )

        #
        # Verify installation flag
        #

        installed = file_system.operations.exists(
            resource=self.INSTALL_FLAG
        )

        if installed:

            print("[INSTALL-MANAGER] Installation detected")

        else:

            print("[INSTALL-MANAGER] Installation not detected")

        return installed