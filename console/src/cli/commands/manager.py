class ManagerCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            self.help()
            return



        if args[0]=="status":

            context.output.info(
                "Manager status"
            )


        elif args[0]=="identify":

            context.output.info(
                "Manager identity"
            )


        else:

            context.output.error(
                "Unknown manager command"
            )



    def help(self):

        print(
"""
manager:

identify

status
"""
        )



def register(router):

    router.register(
        "manager",
        ManagerCommand()
    )