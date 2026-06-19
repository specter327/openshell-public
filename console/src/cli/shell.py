import shlex



class ConsoleShell:



    def __init__(
        self,
        context,
        router
    ):

        self.context=context
        self.router=router



    async def start(self):


        self.context.output.banner(
            "OpenShell Console"
        )


        while True:

            try:


                prompt = (
                    self.context
                    .output
                    .prompt()
                )


                line=input(
                    prompt
                )



                if not line.strip():

                    continue



                args=shlex.split(
                    line
                )



                if args[0] in (
                    "exit",
                    "quit"
                ):

                    self.context.output.warning(
                        "Closing console"
                    )

                    break



                await self.router.dispatch(
                    self.context,
                    args
                )



            except KeyboardInterrupt:

                print()

                self.context.output.warning(
                    "Interrupted"
                )

                break



            except Exception as e:

                self.context.output.error(
                    str(e)
                )