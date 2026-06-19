class SessionsCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        command=args[0]



        if command=="open":

            return await self.open(
                context,
                args[1:]
            )


        if command=="close":

            return await self.close(
                context,
                args[1:]
            )


        if command=="interact":

            return await self.interact(
                context,
                args[1:]
            )


        if command=="query":

            return await self.query(
                context,
                args[1:]
            )


        context.output.error(
            "Unknown sessions command"
        )




    async def open(
        self,
        context,
        args
    ):

        context.output.info(
            "Opening session"
        )


        if not args:

            context.output.warning(
                "sessions open <entity_uid>"
            )

            return



        entity=args[0]


        context.output.info(
            f"Target: {entity}"
        )


        context.output.warning(
            "Not implemented"
        )



    async def close(
        self,
        context,
        args
    ):

        context.output.info(
            "Closing session"
        )


    async def interact(
        self,
        context,
        args
    ):

        context.output.info(
            "Interactive session"
        )



    async def query(
        self,
        context,
        args
    ):

        context.output.info(
            "Query sessions"
        )



    def help(self):

        print(
"""
sessions:

sessions open <entity_uid>

sessions close <session_id>

sessions interact <session_id>

sessions query
"""
        )



def register(router):

    router.register(
        "sessions",
        SessionsCommand()
    )