# ==========================================================
# OpenShell Console
# Authentication Commands
# ==========================================================


def register(router):

    router.register(
        "authentication",
        AuthenticationCommand()
    )



class AuthenticationCommand:



    def execute(
        self,
        context,
        args
    ):


        if len(args) == 0:

            return self.help()



        command = args[0]


        handlers = {

            "client":
                self.client_authenticate,

            "server":
                self.server_authenticate,

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



        context.output.error(
            f"Unknown authentication command: {command}"
        )



    # ======================================================
    # CLIENT AUTHENTICATION
    #
    # State-full
    #
    # Console ---> Manager
    #
    # Stores:
    # runtime.auth_token
    #
    # ======================================================


    async def client_authenticate(
        self,
        context,
        args
    ):


        context.output.info(
            "Authenticating console against manager..."
        )


        manager = (
            context.core
            .services
            .get("manager")
        )


        try:

            auth_token = (
                await manager.client_authenticate()
            )


            if not auth_token:

                context.output.error(
                    "Authentication failed"
                )

                return



            context.core.runtime.set_authentication(
                auth_token
            )



            context.output.success(
                "Console authenticated"
            )


            context.output.info(
                f"Auth token: {auth_token}"
            )


            return True



        except Exception as e:


            context.output.error(
                str(e)
            )


            return False





    # ======================================================
    # SERVER AUTHENTICATION
    #
    # State-less
    #
    # Console ---> Manager
    #
    # No runtime changes
    #
    # ======================================================


    async def server_authenticate(
        self,
        context,
        args
    ):


        context.output.info(
            "Verifying manager identity..."
        )



        manager = (
            context.core
            .services
            .get("manager")
        )


        try:


            result = (
                await manager.server_authenticate()
            )


            if result:

                context.core.runtime.manager_authenticated = True


                context.output.success(
                    "Manager identity verified"
                )


            else:

                context.core.runtime.manager_authenticated = False


                context.output.error(
                    "Manager verification failed"
                )


            return result



        except Exception as e:


            context.output.error(
                str(e)
            )


            return False


    # ======================================================
    # STATUS
    # ======================================================
    def status(
        self,
        context,
        args
    ):


        runtime = (
            context.core
            .runtime
        )


        # ----------------------------------
        # Client authentication
        # ----------------------------------

        if runtime.authenticated:

            context.output.success(
                "Console authentication: OK"
            )


            context.output.info(
                f"Auth token: {runtime.auth_token}"
            )


        else:

            context.output.warning(
                "Console authentication: NOT AUTHENTICATED"
            )



        # ----------------------------------
        # Server authentication
        # ----------------------------------

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
authentication commands:

authentication client

    Authenticate console against manager.
    Stores auth_token.

authentication server

    Verify manager identity.

authentication status

    Show authentication state.

"""
        )