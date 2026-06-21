# ==========================================================
# OpenShell Console
# Passport Commands
# ==========================================================


def register(router):

    router.register(
        "passport",
        PassportCommand()
    )



class PassportCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        if args[0] == "create":


            if len(args) < 2:

                return self.help()


            if args[1] == "open":

                return await self.create_open(
                    context,
                    args[2:]
                )


            context.output.error(
                "Only OPEN passports can be created by console"
            )

            return False



        context.output.error(
            "Unknown passport command"
        )




    async def create_open(
        self,
        context,
        args
    ):


        if not context.core.runtime.auth_token:

            context.output.error(
                "Authentication required"
            )

            return False



        if len(args) != 1:

            context.output.error(
                "Usage: passport create open <domain_uid>"
            )

            return False



        domain_uid = args[0]



        manager = (
            context.core
            .services
            .get("manager")
        )


        try:

            passport = await (
                manager
                .create_open_passport(
                    domain_uid=domain_uid,
                    entity_role="AGENT",
                    expiration_hours=24,
                    usage_limit=1
                )
            )


            context.output.success(
                "OPEN passport created"
            )


            context.output.info(
                f"Passport UID: {passport.uid}"
            )


            context.output.info(
                f"Domain UID: {passport.domain_uid}"
            )


            context.output.warning(
                "Security Code:"
            )


            context.output.info(
                passport.security_code
            )


            return True



        except Exception as e:

            context.output.error(
                str(e)
            )

            return False




    def help(self):

        print(
"""
passport:

passport create open <domain_uid>

    Create OPEN passport.

    CLOSED passports are created
    by the system administrator.

"""
        )