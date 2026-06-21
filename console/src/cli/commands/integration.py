# ==========================================================
# OpenShell Console
# Integration Commands
# ==========================================================


def register(router):

    router.register(
        "integration",
        IntegrationCommand()
    )



class IntegrationCommand:



    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        command = args[0]


        if command == "closed":

            return await self.closed(
                context,
                args[1:]
            )


        context.output.error(
            "Unknown integration command"
        )



    async def closed(
        self,
        context,
        args
    ):


        if not context.core.runtime.auth_token:

            context.output.error(
                "Authentication required"
            )

            return False



        context.output.info(
            "CLOSED integration"
        )


        security_code = input(
            "SECURITY_CODE: "
        )


        manager = (
            context.core
            .services
            .get("manager")
        )


        try:


            result = await (
                manager
                .closed_integration(
                    security_code
                )
            )


            if result.get("integrated"):


                context.output.success(
                    "Integration successful"
                )


                context.output.info(
                    f"Domain: {result.get('domain_uid')}"
                )


                context.output.info(
                    f"Entity: {result.get('entity_uid')}"
                )


                return True



            context.output.error(
                "Integration rejected"
            )


            return False



        except Exception as e:


            context.output.error(
                str(e)
            )


            return False



    def help(self):

        print(
"""
integration:

integration closed

    Integrate console using CLOSED passport.

"""
        )