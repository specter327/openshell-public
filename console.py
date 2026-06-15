#!/usr/bin/env python3

# ==========================================================
# OpenShell Console Integration Test
# ==========================================================
#
# Flow:
#
#   1. Generate/Load Console Identity
#   2. Discover Manager Identity
#   3. Authenticate Console Identity
#   4. Perform CLOSED Integration
#   5. Request Tunnel Service
#
# ==========================================================

# ==========================================================
# LIBRARIES
# ==========================================================

from shared.identity.identification import EntityIdentity
from shared.protocols.negotiation.challenge import ChallengeProtocol
from utils import CommunicationHandler
from shell.client import ShellClient

import requests
import json
import os
import sys
import asyncio


# ==========================================================
# TERMINAL COLORS
# ==========================================================

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"


def header(title):
    print()
    print(f"{Colors.BOLD}{Colors.BLUE}" + "=" * 70)
    print(title)
    print("=" * 70)
    print(Colors.RESET)


def info(message):
    print(f"{Colors.CYAN}[*]{Colors.RESET} {message}")


def success(message):
    print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")


def warning(message):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")


def error(message):
    print(f"{Colors.RED}[-]{Colors.RESET} {message}")


def pretty(data):
    print(json.dumps(data, indent=4, sort_keys=False))


# ==========================================================
# CONFIGURATION
# ==========================================================

SERVER_ADDRESS = "fortaprest.org"
SERVER_PORT = 8000
SERVER_PROTOCOL = "HTTP"

console_uid = ""
console_pik = ""
console_ppik = ""

IDENTITY_FILE = "console_identity.id"


# ==========================================================
# API ROUTES
# ==========================================================

MANAGER_IDENTITY_LOGICAL = "api/v/1/identity/logical"
MANAGER_IDENTITY_PIK = "api/v/1/identity/cryptographic"
ENTITY_TYPE = "api/v/1/identity/type"
SERVER_IDENTITY_AUTH_CHALLENGE = "api/v/1/auth/server/challenge"
CLIENT_IDENTITY_AUTH_CHALLENGE = "api/v/1/auth/client/challenge"
CLIENT_IDENTITY_AUTH_VERIFY = "api/v/1/auth/verify"
CLIENT_INTEGRATION_CLOSED = "api/v/1/integration/closed"
CLIENT_TUNNEL_REQUEST = "api/v/1/services/tunnels/request"
ENTITIES_AGENT_QUERY = "api/v/1/entities/agent/query"
CLIENT_SESSION_REQUEST = "api/v/1/sessions/request"


async def main():
    global console_uid, console_pik, console_ppik
    
    # ==========================================================
    # ENTITY GENERATION / LOADING
    # ==========================================================

    header("CONSOLE IDENTITY")

    regenerate = "--regenerate" in sys.argv

    if not os.path.exists(IDENTITY_FILE) or regenerate:
        info("Generating new Console identity...")
        console_entity = EntityIdentity.generate(name="Console")
        
        console_uid = console_entity.identification.uid
        console_pik = console_entity.cryptographic_identity.public_key
        console_ppik = console_entity.cryptographic_identity.private_key
        
        with open(IDENTITY_FILE, "w") as f:
            json.dump({
                "uid": console_uid,
                "pik": console_pik,
                "ppik": console_ppik
            }, f, indent=4)
        
        success("Console identity generated and saved to disk")
    else:
        info("Loading existing Console identity...")
        with open(IDENTITY_FILE, "r") as f:
            identity_data = json.load(f)
            console_uid = identity_data.get("uid")
            console_pik = identity_data.get("pik")
            console_ppik = identity_data.get("ppik")
        
        success("Console identity loaded successfully")

    print(f"\nUID:\n{console_uid}")
    print(f"\nPUBLIC KEY:\n{console_pik}")
    print(f"\nPRIVATE KEY:\n{console_ppik}")


    # ==========================================================
    # MANAGER DISCOVERY
    # ==========================================================

    header("MANAGER DISCOVERY")

    info("Requesting manager logical identity...")

    manager_uid_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{MANAGER_IDENTITY_LOGICAL}",
        json={
            "entity_uid": console_uid,
            "public_key": console_pik
        }
    )

    manager_uid = manager_uid_request.json().get("uid")

    info("Requesting manager cryptographic identity...")

    manager_pik_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{MANAGER_IDENTITY_PIK}"
    )

    manager_pik = manager_pik_request.json().get("public_key")
    manager_name = manager_pik_request.json().get("name")
    manager_pik_fingerprint = manager_pik_request.json().get("fingerprint")

    info("Requesting manager entity type...")

    manager_type_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{ENTITY_TYPE}"
    )

    manager_type = manager_type_request.json().get("type")

    success("Manager discovered")

    print(f"\nUID         : {manager_uid}")
    print(f"NAME        : {manager_name}")
    print(f"TYPE        : {manager_type}")
    print(f"FINGERPRINT : {manager_pik_fingerprint}")
    print("\nPUBLIC KEY:\n")
    print(manager_pik)


    # ==========================================================
    # CLIENT AUTHENTICATION
    # ==========================================================

    header("CLIENT AUTHENTICATION")

    info("Requesting authentication challenge...")

    client_auth_challenge_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_IDENTITY_AUTH_CHALLENGE}",
        json={
            "entity_uid": console_uid,
            "public_key": console_pik
        }
    )

    client_auth_challenge = client_auth_challenge_request.json().get("challenge")

    success("Challenge received")

    pretty(client_auth_challenge)

    client_auth_challenge_object = ChallengeProtocol.challenge_from_dict(
        client_auth_challenge
    )

    info("Signing challenge...")

    client_auth_signed = ChallengeProtocol.sign(
        private_key=console_ppik,
        challenge=client_auth_challenge_object
    )

    pretty(ChallengeProtocol.response_to_dict(client_auth_signed))

    info("Submitting signed response...")

    client_auth_verify_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_IDENTITY_AUTH_VERIFY}",
        json={
            "challenge_id": client_auth_challenge.get("challenge_id"),
            "response": ChallengeProtocol.response_to_dict(client_auth_signed),
            "entity_uid": console_uid,
            "public_key": console_pik
        }
    )

    verification = client_auth_verify_request.json()

    if verification.get("authenticated"):
        success("Authentication successful")
    else:
        error("Authentication failed")

    pretty(verification)

    client_auth_token = verification.get("auth_token")

    print("\nAUTH TOKEN:\n")
    print(client_auth_token)


    # ==========================================================
    # CLOSED INTEGRATION
    # ==========================================================

    header("CLOSED INTEGRATION")

    warning("Enter CLOSED passport security code")

    security_code = input("\nSECURITY CODE > ")

    client_integration_closed_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_INTEGRATION_CLOSED}",
        headers={
            "Authorization": f"Bearer {client_auth_token}"
        },
        json={
            "security_code": security_code
        }
    )

    integration_result = client_integration_closed_request.json()

    print()

    if integration_result.get("integrated"):
        success("Entity integrated successfully")
    else:
        error("Integration failed")

    pretty(integration_result)


    # ==========================================================
    # TUNNEL REQUEST
    # ==========================================================

    header("TUNNEL NEGOTIATION")

    info("Requesting tunnel service...")

    client_tunnel_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_TUNNEL_REQUEST}",
        json={
            "auth_token": client_auth_token
        }
    )

    client_tunnel_authorization = client_tunnel_request.json().get("ok")
    client_tunnel_port = client_tunnel_request.json().get("tunnel_port")
    client_tunnel_token = client_tunnel_request.json().get("tunnel_token")

    if client_tunnel_authorization:
        success("Tunnel granted")
    else:
        error("Tunnel denied")

    print(f"\nTunnel Token : {client_tunnel_token}")
    print(f"Tunnel Port  : {client_tunnel_port}")
    print(f"Tunnel Addr  : {SERVER_ADDRESS}:{client_tunnel_port}")

    print("")
    # Query for available entities
    info(f"Available entities:")
    client_agents_query_request = requests.post(
    	f"{SERVER_PROTOCOL.lower()}://{SERVER_ADDRESS}:{SERVER_PORT}/{ENTITIES_AGENT_QUERY}",
    	json={
    		"auth_token":client_auth_token
    	}
    )

    if len(client_agents_query_request.json().get("entities")) == 0: error("Any entity available")
    else: 
        for entity in client_agents_query_request.json().get("entities"): 
            info(f"    Entity UID: {entity.get('entity_uid')}")
            info(f"    Domain UID: {entity.get('domain_uid')}")
            info(f"    Entity type: {entity.get('entity_type')}")
            info(f"    Entity role: {entity.get('role')}")
            info(f"    Entity status: {entity.get('status')}")

    # ==========================================================
    # READY
    # ==========================================================

    header("SESSION READY")

    success("Console integrated and operational")

    print(f"\nTunnel endpoint:\n{SERVER_ADDRESS}:{client_tunnel_port}\n")

    communication = CommunicationHandler(
        auth_token=client_auth_token,
        tunnel_token=client_tunnel_token,
        tunnel_port=client_tunnel_port,
        tunnel_host=SERVER_ADDRESS
    )

    await communication.connect()

    # Request session with the selected agent
    info("Specify the agent to establish connection:")
    agent_uid = input(">>> ")

    info(f"Selected agent: {agent_uid}")
    client_session_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://{SERVER_ADDRESS}:{SERVER_PORT}/{CLIENT_SESSION_REQUEST}",
        json={
            "auth_token":client_auth_token,
            "tunnel_token":client_tunnel_token,
            "destination_uid":agent_uid
        }
    )

    session_request_result = client_session_request.json()
    session_response = session_request_result.get("ok")

    if session_response:
        info("Session established successfully")
        client_session_token = session_request_result.get("session_token")
        source_entity = session_request_result.get("source_uid")
        destination_entity = session_request_result.get("destination_uid")
        authorized_date = session_request_result.get("authorized_date")

        info(f"Source entity: {source_entity} | Destination entity: {destination_entity} | Authorized date: {authorized_date}")
        shell_client = ShellClient(
            communication_handler=communication,
            auth_token=client_auth_token,
            tunnel_token=client_tunnel_token,
            session_token=client_session_token
        )

        await shell_client.start()

    else:
        error("Session denied")
        return


if __name__ == "__main__":
    asyncio.run(main())