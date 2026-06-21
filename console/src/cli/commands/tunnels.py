# ==========================================================
# OpenShell Console
# Tunnel Commands
# ==========================================================


def register(router):

    router.register(
        "tunnels",
        TunnelsCommand()
    )



class TunnelsCommand:



    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        command = args[0]


        handlers = {


            "request":
                self.request,


            "status":
                self.status,


            "clear":
                self.clear

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
            "Unknown tunnels command"
        )



    # ======================================================
    # REQUEST
    # ======================================================


    async def request(
        self,
        context,
        args
    ):


        context.output.info(
            "Requesting tunnel..."
        )


        manager = (
            context.core
            .services
            .get("tunnel")
        )


        if not manager:

            context.output.error(
                "Tunnel subsystem unavailable"
            )

            return



        try:


            tunnel = await (
                manager
                .request_tunnel()
            )


            context.output.success(
                "Tunnel authorized"
            )


            print()


            context.output.info(
                f"Token: {tunnel.get('tunnel_token')}"
            )


            context.output.info(
                f"Host: {context.core.runtime.manager_address}"
            )


            context.output.info(
                f"Port: {tunnel.get('tunnel_port')}"
            )



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


        manager = (
            context.core
            .services
            .get("tunnel")
        )


        if not manager:

            context.output.error(
                "Tunnel subsystem unavailable"
            )

            return



        status = (
            manager
            .status()
        )


        if not status.get(
            "authorized"
        ):


            context.output.warning(
                "No active tunnel"
            )

            return



        context.output.info(
            "Tunnel active"
        )


        context.output.info(
            f"Token: {status.get('token')}"
        )


        context.output.info(
            f"Host: {status.get('host')}"
        )


        context.output.info(
            f"Port: {status.get('port')}"
        )



    # ======================================================
    # CLEAR
    # ======================================================


    async def clear(
        self,
        context,
        args
    ):


        runtime = (
            context.core
            .runtime
        )


        runtime.clear_tunnel()


        context.output.success(
            "Tunnel cleared"
        )



    # ======================================================
    # HELP
    # ======================================================


    def help(self):


        print(
"""
tunnels commands:


tunnels request

    Request a new communication tunnel.


tunnels status

    Show current tunnel.


tunnels clear

    Clear runtime tunnel state.

"""
        )