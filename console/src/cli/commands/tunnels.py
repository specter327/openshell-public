class TunnelsCommand:


    async def execute(
        self,
        context,
        args
    ):

        if not args:

            return self.help()



        cmd=args[0]


        if cmd=="request":

            context.output.info(
                "Request tunnel"
            )

        elif cmd=="query":

            context.output.info(
                "Query tunnels"
            )

        elif cmd=="close":

            context.output.info(
                "Close tunnel"
            )

        elif cmd=="status":

            context.output.info(
                "Tunnel status"
            )

        else:

            context.output.error(
                "Unknown tunnel command"
            )



    def help(self):

        print(
"""
tunnels:

request

query

close

status
"""
        )



def register(router):

    router.register(
        "tunnels",
        TunnelsCommand()
    )