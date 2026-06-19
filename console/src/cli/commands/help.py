# ==========================================================
# OpenShell Console CLI
# Help Command
# ==========================================================


def register(router):

    router.register(
        "help",
        HelpCommand()
    )



class HelpCommand:


    def execute(
        self,
        context,
        args
    ):

        self.show()



    def show(self):

        print(
"""
============================================================
 OpenShell Console Help
============================================================

SYSTEM:

 help
 version
 about


MANAGER:

 manager identify
 manager authenticate
 manager status


IDENTITY:

 identity create
 identity show
 identity export <directory>
 identity status


DOMAINS:

 domains query
 domains integrate


TUNNELS:

 tunnels request
 tunnels query
 tunnels close
 tunnels status


SESSIONS:

 sessions open <entity_uid>
 sessions close <session_id>
 sessions interact <session_id>
 sessions query


SUPPORT:

 support diagnostic network
 support diagnostic identity
 support diagnostic manager
 support diagnostic tunnels
 support diagnostic sessions
 support diagnostic runtime
 support diagnostic events


EXAMPLES:

 console> identity create

 console> identity show

 console> manager status

 console> support diagnostic runtime


============================================================
"""
        )