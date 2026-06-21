# ==========================================================
# OpenShell Console CLI
# Identity Commands
# ==========================================================


from shared.identity.identification import (
    EntityIdentity
)

from pathlib import Path



def register(router):

    router.register(
        "identity",
        IdentityCommand()
    )



class IdentityCommand:



    def execute(
        self,
        context,
        args
    ):


        if len(args) == 0:

            return self.help()



        command = args[0]



        handlers = {

            "show":
                self.show,

            "create":
                self.create,

            "export":
                self.export,

            "status":
                self.status

        }



        handler = handlers.get(
            command
        )



        if handler:

            return handler(
                context,
                args[1:]
            )



        print(
            f"[!] Unknown identity command: {command}"
        )



    # ======================================================
    # SHOW
    # ======================================================


    def show(
        self,
        context,
        args
    ):

        #print(context.core.runtime.console_profile)
        console_profile = context.core.runtime.console_profile
        console_public_profile = console_profile.get("public")
        console_private_profile = console_profile.get("private")
        print(f"[*] Console UID: {console_public_profile.get('identification').get('uid')}")
        print(f"[*] Console PIK: {console_public_profile.get('cryptographic_identity').get('public_key')}")
        print(f"[*] Console name: {console_public_profile.get('name')}")
        print(f"[*] PIK Algorithm: {console_public_profile.get('cryptographic_identity').get('algorithm')}")
        print(f"[*] PIK fingerprint: {console_public_profile.get('cryptographic_identity').get('fingerprint')}")




    # ======================================================
    # CREATE
    # ======================================================


    def create(
        self,
        context,
        args
    ):


        if context.identity_exists():

            print(
                "[!] Identity already exists"
            )

            return



        print(
            "[*] Creating console identity"
        )



        entity = (
            EntityIdentity.generate(
                name="Console"
            )
        )



        public = (
            entity.export_public()
        )


        private = (
            entity.to_dict()
        )



        metadata = {

            "type":
                "CONSOLE",

            "version":
                1

        }



        context.identity_store.save(

            public_profile=public,

            private_profile=private,

            metadata=metadata

        )



        print(
            "[+] Identity created"
        )




    # ======================================================
    # EXPORT
    # ======================================================


    def export(
        self,
        context,
        args
    ):


        if len(args)==0:

            print(
                "Usage:"
            )

            print(
                "identity export <path>"
            )

            return



        path = Path(
            args[0]
        )



        exported = (
            context
            .identity_store
            .export_public(
                path
            )
        )


        print(
            "[+] Identity exported:"
        )

        print(
            exported
        )




    # ======================================================
    # STATUS
    # ======================================================


    def status(
        self,
        context,
        args
    ):


        if context.identity_exists():

            print(
                "[+] Identity available"
            )

        else:

            print(
                "[-] Identity missing"
            )




    # ======================================================
    # HELP
    # ======================================================


    def help(self):

        print(
"""
identity commands:

identity create

identity show

identity export <directory>

identity status

"""
        )