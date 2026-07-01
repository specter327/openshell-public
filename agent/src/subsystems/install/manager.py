# Library import
from pathlib import Path
import shutil
import shlex

import fsresource_tree as fs

from ..service import Subsystem


class InstallationManager(Subsystem):

    INSTALL_FLAG = fs.File(
        name="installed",
        extension="flag"
    )

    ELEMENT_NAME: str = "INSTALLATION-MANAGER"

    # =====================================================
    # PROGRAM
    # =====================================================

    def get_program_resource(self) -> fs.File:

        return fs.File(
            name="agent"
        )

    # =====================================================
    # PRIVATE
    # =====================================================

    def _install_program(
        self,
        destination: Path
    ) -> None:
        """
        Install the executable program.

        Development:
            Create launcher script.

        Frozen:
            Copy packaged executable.
        """

        #
        # Frozen executable
        #

        if self.environment.frozen:

            shutil.copy2(
                self.environment.entrypoint,
                destination
            )

            destination.chmod(0o755)

            return

        #
        # Development launcher
        #

        command = " ".join(
            shlex.quote(argument)
            for argument in self.environment.command
        )

        launcher = (
            "#!/usr/bin/env bash\n\n"
            f'exec {command} "$@"\n'
        )

        destination.write_text(
            launcher,
            encoding="utf-8"
        )

        destination.chmod(0o755)

    # =====================================================
    # INSTALL
    # =====================================================

    async def install(self) -> fs.File:

        storage_service = self.core.services.get("storage")
        logger_service = self.services.get("logger")

        logger_service.info(
            source=self.ELEMENT_NAME,
            message="Starting installation"
        )

        if await self.is_installed():

            logger_service.warning(
                source=self.ELEMENT_NAME,
                message="Installation currently detected"
            )

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
        # Create executable
        #

        file_system.operations.create(
            resource=program,
            recursive_parent=True
        )

        #
        # Install executable / launcher
        #

        destination = Path(
            file_system.operations.path(program)
        )

        self._install_program(
            destination
        )

        print(
            "[INSTALL-MANAGER] Program installed: "
            f"{destination}"
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

        logger_service.info(
            source=self.ELEMENT_NAME,
            message="Installation complete"
        )

        return program

    # =====================================================
    # UNINSTALL
    # =====================================================

    async def uninstall(self) -> bool:

        storage_service = self.core.services.get("storage")
        logger_service = self.services.get("logger")

        logger_service.info(
            source=self.ELEMENT_NAME,
            message="Starting uninstallation"
        )

        print(
            "[INSTALL-MANAGER] Deleting: "
            f"{storage_service.storage_schema.file_system.operations.path(storage_service.storage_schema.AGENT_ROOT)}..."
        )

        storage_service.storage_schema.file_system.operations.delete(
            resource=storage_service.storage_schema.AGENT_ROOT,
            recursive_children=True,
            purge=True
        )

        print(
            "[INSTALL-MANAGER] Directory successfully deleted"
        )

        logger_service.info(
            source=self.ELEMENT_NAME,
            message="Finishing uninstallation"
        )

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

            print(
                "[INSTALL-MANAGER] Installation detected"
            )

        else:

            print(
                "[INSTALL-MANAGER] Installation not detected"
            )

        return installed