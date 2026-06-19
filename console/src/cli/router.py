# ==========================================================
# OpenShell Console CLI
# Command Router
# ==========================================================

import inspect


class CommandRouter:


    def __init__(self):

        self.commands = {}



    def register(self, name, command):

        self.commands[name] = command



    async def dispatch(self, context, args):


        if len(args) == 0:
            return



        command = args[0]

        handler = self.commands.get(command)


        if handler is None:

            context.output.error(
                f"Unknown command: {command}"
            )

            return



        result = handler.execute(
            context,
            args[1:]
        )


        # Si devuelve coroutine, esperar
        if inspect.isawaitable(result):

            return await result


        # Si es normal, continuar
        return result