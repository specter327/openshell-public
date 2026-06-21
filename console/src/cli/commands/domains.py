# ==========================================================
# OpenShell Console
# Domain Commands
# ==========================================================


def register(router):

    router.register(
        "domains",
        DomainsCommand()
    )



class DomainsCommand:



    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        command = args[0]


        handlers = {

            "list":
                self.list_domains,

            "status":
                self.status

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
            "Unknown domains command"
        )



    async def list_domains(
        self,
        context,
        args
    ):


        context.output.info(
            "Querying domains..."
        )


        manager = (
            context.core
            .services
            .get("domain")
        )


        try:

            domains = await (
                manager.query()
            )


            if not domains:

                context.output.warning(
                    "No domains available"
                )

                return



            context.output.success(
                f"Domains: {len(domains)}"
            )


            for domain in domains:

                print()

                context.output.info(f"Domain UID: {domain}")

                #context.output.info(
                #    f"UID: {domain.uid}"
                #)

                #context.output.info(
                #    f"Name: {domain.name}"
                #)



        except Exception as e:

            context.output.error(
                str(e)
            )



    async def status(
        self,
        context,
        args
    ):


        runtime = (
            context.core.runtime
        )


        if runtime.current_domain_uid:

            context.output.info(
                f"Current domain: {runtime.current_domain_uid}"
            )

        else:

            context.output.warning(
                "No domain selected"
            )



    def help(self):

        print(
"""
domains commands:

domains list

    List available domains.


domains status

    Show current domain.

"""
        )