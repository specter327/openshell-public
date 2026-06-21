# ==========================================================
# OpenShell Console
# Core Runtime State
# ==========================================================


class CoreRuntime:
    """
    Runtime state shared by all subsystems.

    This object stores volatile execution data.

    Rules:
    - No business logic
    - No network logic
    - No filesystem logic
    - No persistence

    Runtime data is lost when the process exits.
    """


    def __init__(self):

        self.reset()


    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        #
        # Manager
        #

        self.manager_uid = None
        self.manager_name = None
        self.manager_type = None
        self.manager_public_key = None
        self.manager_fingerprint = None
        self.manager_address: str = None
        self.manager_port: str = None
        self.manager_protocol: str = None
        self.manager_authenticated: bool = False


        #
        # Authentication
        #

        self.authenticated = False

        self.auth_token = None


        #
        # Tunnel
        #

        self.tunnel_authorized = False
        self.communication_connected: bool = False

        self.tunnel_token = None
        self.tunnel_host = None
        self.tunnel_port = None


        #
        # Session
        #

        self.session_active = False

        self.session_uid = None
        self.session_token = None

        self.source_uid = None
        self.destination_uid = None

        self.sessions: list = []


        #
        # Domain
        #

        self.current_domain_uid = None


        #
        # Console
        #

        self.console_ready = False
        self.console_profile: Dict = None


    # ======================================================
    # AUTH
    # ======================================================
    def set_manager_address(self, manager_address: str) -> bool:
        self.manager_address = manager_address
        return True

    def set_manager_port(self, manager_port: int) -> bool:
        self.manager_port = manager_port
        return True

    def set_manager_protocol(self, manager_protocol: str) -> bool:
        self.manager_protocol = manager_protocol
        return True

    def set_console_profile(self, console_profile: dict):
        self.console_profile = console_profile

        return True
    
    def set_authentication(
        self,
        auth_token
    ):

        self.authenticated = True
        self.auth_token = auth_token


    def clear_authentication(self):

        self.authenticated = False
        self.auth_token = None


    # ======================================================
    # TUNNEL
    # ======================================================

    def set_tunnel(
        self,
        tunnel_token,
        tunnel_host,
        tunnel_port
    ):

        self.tunnel_authorized = True

        self.tunnel_token = tunnel_token
        self.tunnel_host = tunnel_host
        self.tunnel_port = tunnel_port


    def clear_tunnel(self):

        self.tunnel_authorized = False

        self.tunnel_token = None
        self.tunnel_host = None
        self.tunnel_port = None


    # ======================================================
    # SESSION
    # ======================================================

    def set_session(
        self,
        session_uid,
        session_token,
        source_uid,
        destination_uid
    ):

        self.session_active = True

        self.session_uid = session_uid
        self.session_token = session_token

        self.source_uid = source_uid
        self.destination_uid = destination_uid


    def clear_session(self):

        self.session_active = False

        self.session_uid = None
        self.session_token = None

        self.source_uid = None
        self.destination_uid = None


    # ======================================================
    # MANAGER
    # ======================================================

    def set_manager_identity(
        self,
        uid,
        name,
        entity_type,
        public_key,
        fingerprint
    ):

        self.manager_uid = uid
        self.manager_name = name
        self.manager_type = entity_type
        self.manager_public_key = public_key
        self.manager_fingerprint = fingerprint


    # ======================================================
    # EXPORT
    # ======================================================

    def to_dict(self):

        return {

            "manager": {

                "uid":
                    self.manager_uid,

                "name":
                    self.manager_name,

                "type":
                    self.manager_type,

                "public_key":
                    self.manager_public_key,

                "fingerprint":
                    self.manager_fingerprint
            },

            "authentication": {

                "authenticated":
                    self.authenticated,

                "auth_token":
                    self.auth_token
            },

            "tunnel": {

                "authorized":
                    self.tunnel_authorized,

                "host":
                    self.tunnel_host,

                "port":
                    self.tunnel_port,

                "token":
                    self.tunnel_token
            },

            "session": {

                "active":
                    self.session_active,

                "session_uid":
                    self.session_uid,

                "session_token":
                    self.session_token,

                "source_uid":
                    self.source_uid,

                "destination_uid":
                    self.destination_uid
            },

            "domain": {

                "current_domain_uid":
                    self.current_domain_uid
            }
        }