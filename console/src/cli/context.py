# ==========================================================
# OpenShell Console Context
# ==========================================================


from pathlib import Path

from shared.identity.store import IdentityStore
from .output import ConsoleOutput


class ConsoleContext:


    def __init__(self):


        self.base_path = Path(
            __file__
        ).resolve().parents[2]


        self.storage_path = (
            self.base_path /
            "storage"
        )


        self.identity_store = IdentityStore(

            base_path=self.storage_path,

            namespace="console"

        )


        self.authenticated = False

        self.auth_token = None

        self.output = ConsoleOutput(
            enable_colors=True
        )



    # ------------------------------------------------------

    def identity_exists(self):

        return (
            self.identity_store.exists()
        )


    # ------------------------------------------------------

    def load_identity(self):

        return (
            self.identity_store.load()
        )