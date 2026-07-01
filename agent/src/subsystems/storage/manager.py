# Library import
from pathlib import Path

from ..service import Subsystem

import fsresource_tree as fs


# ==========================================================
# STORAGE SCHEMA (GNU/Linux)
# ==========================================================

class StorageSchemaLinux:

    def __init__(self):

        self.file_system = fs

        #
        # Storage structure definition
        #

        self.storage_tree = fs.ResourceTree(
            name="Storage System",
            description="GNU/Linux Storage System"
        )

        #
        # Root
        #

        self.UNIT_ROOT = fs.Directory(name="/")

        self.storage_tree.register(
            self.UNIT_ROOT
        )

        #
        # Build the real HOME path.
        #
        # Examples:
        #
        #   /home/specter
        #   /root
        #   /var/lib/postgresql
        #

        home = Path.home().resolve()

        current = self.UNIT_ROOT

        self.HOME_DIRECTORIES = []

        for part in home.parts[1:]:

            directory = fs.Directory(
                name=part
            )

            self.storage_tree.register(
                directory,
                parent=current
            )

            self.HOME_DIRECTORIES.append(
                directory
            )

            current = directory

        #
        # User home directory
        #

        self.USER_DIR = current

        #
        # OpenShell root
        #

        self.AGENT_ROOT = fs.Directory(
            name=".osa"
        )

        self.storage_tree.register(
            self.AGENT_ROOT,
            parent=self.USER_DIR
        )

        #
        # Data
        #

        self.DATA_ROOT = fs.Directory(
            name="data"
        )

        self.storage_tree.register(
            self.DATA_ROOT,
            parent=self.AGENT_ROOT
        )

        #
        # Software
        #

        self.SOFTWARE_ROOT = fs.Directory(
            name="software"
        )

        self.storage_tree.register(
            self.SOFTWARE_ROOT,
            parent=self.AGENT_ROOT
        )


# ==========================================================
# STORAGE MANAGER
# ==========================================================

class StorageManager(Subsystem):

    def __init__(
        self,
        core
    ):

        super().__init__(core)

        self.storage_schema = None

    async def start(self):

        #
        # Adapt according to operating system
        #

        self.storage_schema = StorageSchemaLinux()

    async def stop(self):
        pass


# ==========================================================
# STORAGE RUNTIME
# ==========================================================

class StorageRuntime:
    pass