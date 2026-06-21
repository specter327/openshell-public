# ==========================================================
# OpenShell Console
# Manager Commands
# ==========================================================


from ...shared.api.manager.v1 import OSAMClient



def register(router):

    router.register(
        "manager",
        ManagerCommand()
    )




class ManagerCommand:



    async def execute(
        self,
        context,
        args
    ):


        if not args:

            self.help()
            return



        command = args[0]



        handlers = {

            "identify":
                self.identify,

            "status":
                self.status,

            "config":
                self.config

        }



        handler = handlers.get(
            command
        )



        if handler:

            return await handler(
                context,
                args[1:]
            )



        context.output.error(
            "Unknown manager command"
        )




    # ======================================================
    # IDENTIFY
    #
    # Query manager identity
    #
    # ======================================================


    async def identify(
        self,
        context,
        args
    ):


        runtime = (
            context.core
            .runtime
        )


        if not runtime.manager_address:

            context.output.error(
                "Manager address not configured"
            )

            return


        client = OSAMClient(

            host=runtime.manager_address,

            port=runtime.manager_port,

            protocol=runtime.manager_protocol
        )


        try:


            logical = (
                await client.identity
                .get_logical_identity()
            )


            crypto = (
                await client.identity
                .get_cryptographic_identity()
            )


            entity_type = (
                await client.identity
                .get_entity_type()
            )



            runtime.set_manager_identity(

                uid=logical.uid,

                name=getattr(
                    logical,
                    "name",
                    None
                ),

                entity_type=entity_type.type,

                public_key=crypto.public_key,

                fingerprint=getattr(
                    crypto,
                    "fingerprint",
                    None
                )
            )



            context.output.success(
                "Manager identity loaded"
            )


            context.output.info(
                f"UID: {runtime.manager_uid}"
            )


            context.output.info(
                f"Type: {runtime.manager_type}"
            )


            context.output.info(
                f"PIK: {runtime.manager_public_key}"
            )


            return True



        except Exception as e:


            context.output.error(
                str(e)
            )


            return False





    # ======================================================
    # CONFIG
    #
    # manager config address <value>
    # manager config port <value>
    # manager config protocol <http|https>
    #
    # ======================================================


    async def config(
        self,
        context,
        args
    ):


        if len(args) < 2:

            context.output.error(
                "Usage: manager config <key> <value>"
            )

            return



        key = args[0]

        value = args[1]



        runtime = (
            context.core
            .runtime
        )



        if key == "address":


            runtime.set_manager_address(
                value
            )


        elif key == "port":


            runtime.set_manager_port(
                int(value)
            )


        elif key == "protocol":


            protocol = (
                value.lower()
            )


            if protocol not in (
                "http",
                "https"
            ):

                context.output.error(
                    "Protocol must be HTTP or HTTPS"
                )

                return


            runtime.set_manager_protocol(
                protocol
            )


        else:

            context.output.error(
                "Unknown manager config option"
            )

            return



        context.output.success(
            "Manager configuration updated"
        )




    # ======================================================
    # STATUS
    #
    # Runtime only
    #
    # ======================================================


    async def status(
        self,
        context,
        args
    ):


        runtime = (
            context.core
            .runtime
        )


        context.output.info(
            f"Address: {runtime.manager_address}"
        )


        context.output.info(
            f"Port: {runtime.manager_port}"
        )


        context.output.info(
            f"Protocol: {runtime.manager_protocol}"
        )


        context.output.info(
            f"UID: {runtime.manager_uid}"
        )


        context.output.info(
            f"Type: {runtime.manager_type}"
        )


        if runtime.manager_authenticated:


            context.output.success(
                "Manager authentication: VERIFIED"
            )

        else:

            context.output.warning(
                "Manager authentication: NOT VERIFIED"
            )





    # ======================================================
    # HELP
    # ======================================================


    def help(self):

        print(
"""
manager commands:

manager config address <ip>

manager config port <port>

manager config protocol <http|https>


manager identify

manager status

"""
        )