def register(router):

    router.register(
        "shell",
        ShellCommand()
    )


class ShellCommand:

    async def execute(
        self,
        context,
        args
    ):

        runtime = (
            context.core.runtime
        )

        if not runtime.session_token:

            context.output.error(
                "No active session"
            )

            return

        app = (
            context.core.services
            .get("app")
        )

        try:

            await app.run(
                "shell",
                session_token=runtime.session_token
            )

        except Exception as e:

            context.output.error(
                str(e)
            )