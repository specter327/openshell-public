# ==========================================================
# OpenShell Console
# Commands - Communication
# ==========================================================

def register(router):

    router.register(
        "communication",
        CommunicationCommand()
    )

class CommunicationCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()


        command = args[0]


        handlers = {

            "connect":
                self.connect,

            "disconnect":
                self.disconnect,

            "status":
                self.status,

            "reconnect":
                self.reconnect
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
            "Unknown communication command"
        )



    # ======================================================
    # CONNECT
    # ======================================================

    async def connect(
        self,
        context,
        args
    ):


        context.output.info(
            "Connecting communication channel..."
        )


        communication = (
            context.core
            .services
            .get("communication")
        )


        try:

            result = await (
                communication
                .connect()
            )


            if result:

                context.output.success(
                    "Communication connected"
                )


            return result


        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # DISCONNECT
    # ======================================================

    async def disconnect(
        self,
        context,
        args
    ):


        context.output.info(
            "Closing communication channel..."
        )


        communication = (
            context.core
            .services
            .get("communication")
        )


        try:

            result = await (
                communication
                .close()
            )


            context.output.success(
                "Communication disconnected"
            )


            return result


        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # STATUS
    # ======================================================

    async def status(
        self,
        context,
        args
    ):


        communication = (
            context.core
            .services
            .get("communication")
        )


        status = (
            communication
            .status()
        )


        context.output.info(
            f"Connected: {status['connected']}"
        )

        context.output.info(
            f"Authenticated: {status['authenticated']}"
        )

        context.output.info(
            f"Tunnel authorized: {status['tunnel_authorized']}"
        )


        return status



    # ======================================================
    # RECONNECT
    # ======================================================

    async def reconnect(
        self,
        context,
        args
    ):


        communication = (
            context.core
            .services
            .get("communication")
        )


        try:

            result = await (
                communication
                .reconnect()
            )


            context.output.success(
                "Communication reconnected"
            )


            return result


        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # HELP
    # ======================================================

    def help(
        self
    ):

        return """

communication commands:

communication connect

    Open communication channel.


communication disconnect

    Close communication channel.


communication status

    Show communication state.


communication reconnect

    Reconnect channel.

"""