# ==========================================================
# OpenShell Console
# Entity Commands
# ==========================================================


def register(router):

    router.register(
        "entities",
        EntityCommand()
    )



class EntityCommand:


    async def execute(
        self,
        context,
        args
    ):

        if not args:

            return self.help()


        command = args[0]


        if command == "query":

            return await self.query(
                context,
                args[1:]
            )


        context.output.error(
            "Unknown entities command"
        )


        return False



    # ======================================================
    # QUERY
    # ======================================================

    async def query(
        self,
        context,
        args
    ):


        if not context.core.runtime.auth_token:

            context.output.error(
                "Authentication required"
            )

            return False



        entity_type = None


        if args:

            entity_type = args[0].upper()



        manager = (
            context.core
            .services
            .get("manager")
        )


        try:

            entities = await (
                manager
                .query_entities(
                    entity_type=entity_type
                )
            )


            if not entities:

                context.output.warning(
                    "No entities available"
                )

                return True



            context.output.info(
                "Available entities:"
            )


            for entity in entities:


                context.output.info(
                    ""
                )


                context.output.info(
                    f"UID: {entity.get('entity_uid')}"
                )


                context.output.info(
                    f"TYPE: {entity.get('entity_type')}"
                )


                context.output.info(
                    f"ROLE: {entity.get('role')}"
                )


                context.output.info(
                    f"DOMAIN: {entity.get('domain_uid')}"
                )


                context.output.info(
                    f"STATUS: {entity.get('status')}"
                )


            return True



        except Exception as e:


            context.output.error(
                str(e)
            )


            return False



    # ======================================================
    # HELP
    # ======================================================

    def help(self):

        print(
"""
entities:

entities query

    Query all visible entities.


entities query <TYPE>

    Query entities filtered by type.

Examples:

    entities query AGENT

"""
        )