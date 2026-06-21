# ==========================================================
# OpenShell Console
# Session Commands
# ==========================================================


def register(router):

    router.register(
        "sessions",
        SessionsCommand()
    )



class SessionsCommand:


    async def execute(
        self,
        context,
        args
    ):


        if not args:

            return self.help()



        command = args[0]


        handlers = {

            "create":
                self.create_session,

            "list":
                self.list_sessions,

            "status":
                self.status,

            "close":
                self.close_session

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
            "Unknown sessions command"
        )



    # ======================================================
    # CREATE
    # ======================================================


    async def create_session(
        self,
        context,
        args
    ):


        if not args:

            context.output.error(
                "Usage: sessions create <destination_uid>"
            )

            return



        destination_uid = args[0]


        manager = (
            context.core
            .services
            .get("session")
        )


        context.output.info(
            "Creating session..."
        )


        try:

            session = await (
                manager.create(
                    destination_uid
                )
            )


            context.output.success(
                "Session created"
            )


            print()

            context.output.info(
                f"Session UID: {session.get('session_uid')}"
            )

            context.output.info(
                f"Source: {session.get('source_uid')}"
            )

            context.output.info(
                f"Destination: {session.get('destination_uid')}"
            )

            context.output.info(
                f"Session Token: {session.get('session_token')}"
            )



        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # LIST
    # ======================================================


    async def list_sessions(
        self,
        context,
        args
    ):


        manager = (
            context.core
            .services
            .get("session")
        )


        context.output.info(
            "Querying sessions..."
        )


        try:

            sessions = await (
                manager.list()
            )


            if not sessions:

                context.output.warning(
                    "No active sessions"
                )

                return



            context.output.success(
                f"Sessions: {len(sessions)}"
            )



            for session in sessions:

                print()

                context.output.info(
                    f"Session UID: {session.get('session_uid')}"
                )

                context.output.info(
                    f"Source: {session.get('source_uid')}"
                )

                context.output.info(
                    f"Destination: {session.get('destination_uid')}"
                )

                context.output.info(
                    f"Token: {session.get('session_token')}"
                )



        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # STATUS
    # ======================================================


    async def status(
        self,
        context,
        args
    ):


        manager = (
            context.core
            .services
            .get("session")
        )


        status = (
            manager.status()
        )


        if not status.get(
            "active"
        ):

            context.output.warning(
                "No active session"
            )

            return



        context.output.success(
            "Active session"
        )


        print()


        context.output.info(
            f"Session UID: {status.get('session_uid')}"
        )

        context.output.info(
            f"Token: {status.get('session_token')}"
        )

        context.output.info(
            f"Source: {status.get('source_uid')}"
        )

        context.output.info(
            f"Destination: {status.get('destination_uid')}"
        )



    # ======================================================
    # CLOSE
    # ======================================================


    async def close_session(
        self,
        context,
        args
    ):


        session_token = None


        if args:

            session_token = args[0]



        manager = (
            context.core
            .services
            .get("session")
        )


        context.output.info(
            "Closing session..."
        )


        try:

            result = await (
                manager.close(
                    session_token
                )
            )


            if result.get(
                "closed"
            ) or result.get(
                "ok"
            ):


                context.output.success(
                    "Session closed"
                )


            else:

                context.output.warning(
                    "Session close response received"
                )


            return result



        except Exception as e:

            context.output.error(
                str(e)
            )



    # ======================================================
    # HELP
    # ======================================================


    def help(self):

        print(
"""
sessions commands:

sessions create <destination_uid>

    Create a new shell session.


sessions list

    List active sessions.


sessions status

    Show current session.


sessions close [session_token]

    Close session.

"""
        )