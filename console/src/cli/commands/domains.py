class DomainsCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        if args[0]=="query":

            context.output.info(
                "Query domains"
            )


        elif args[0]=="integrate":

            context.output.info(
                "Integrate domain"
            )


        else:

            context.output.error(
                "Unknown domains command"
            )



    def help(self):

        print(
"""
domains:

query

integrate
"""
        )



def register(router):

    router.register(
        "domains",
        DomainsCommand()
    )