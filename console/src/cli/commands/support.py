class SupportCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        if args[0]=="diagnostic":

            context.output.info(
                "Running diagnostics"
            )

        elif args[0]=="help":
            self.help()



    def help(self):

        print(
"""
support:

diagnostic
"""
        )



def register(router):

    router.register(
        "support",
        SupportCommand()
    )