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


    #
    # Usage limit
    #

    while True:

        value = input(
            "Usage limit (1-50): "
        ).strip()

        try:

            usage_limit = int(value)

        except ValueError:

            context.output.error(
                "Usage limit must be an integer."
            )

            continue


        if usage_limit < 1 or usage_limit > 50:

            context.output.error(
                "Usage limit must be between 1 and 50."
            )

            continue

        break


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
                usage_limit=usage_limit
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


        context.output.info(
            f"Usage limit: {passport.usage_limit}"
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