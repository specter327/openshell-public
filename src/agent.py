#!/usr/bin/env python3

# ==========================================================
# OpenShell Agent Integration Test
# ==========================================================
#
# Flow:
#
#   1. Generate/Load Agent Identity
#   2. Discover Manager Identity
#   3. Authenticate Agent Identity
#   4. Perform OPEN Integration
#   5. Request Tunnel Service
#
# ==========================================================

# ==========================================================
# LIBRARIES
# ==========================================================

from shared.identity.identification import EntityIdentity
from shared.protocols.negotiation.challenge import ChallengeProtocol
from utils import CommunicationHandler
from shell.server import ShellServer

import requests
import json
import os
import sys
import asyncio
import time


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

agent_uid = ""
agent_pik = ""
agent_ppik = ""

IDENTITY_FILE = "agent_identity.id"


# ==========================================================
# API ROUTES
# ==========================================================

MANAGER_IDENTITY_LOGICAL = "api/v/1/identity/logical"
MANAGER_IDENTITY_PIK = "api/v/1/identity/cryptographic"
ENTITY_TYPE = "api/v/1/identity/type"

CLIENT_IDENTITY_AUTH_CHALLENGE = (
    "api/v/1/auth/client/challenge"
)

CLIENT_IDENTITY_AUTH_VERIFY = (
    "api/v/1/auth/verify"
)

CLIENT_INTEGRATION_OPEN = (
    "api/v/1/integration/open"
)

CLIENT_TUNNEL_REQUEST = (
    "api/v/1/services/tunnels/request"
)


async def main():

    global agent_uid
    global agent_pik
    global agent_ppik

    # ==========================================================
    # CLI ARGUMENT PARSING
    # ==========================================================

    regenerate = "--regenerate" in sys.argv
    integrate_mode = False
    security_code = None

    if "--integrate" in sys.argv:
        integrate_mode = True
        try:
            idx = sys.argv.index("--integrate")
            if idx + 1 < len(sys.argv):
                val = sys.argv[idx + 1]
                if val.startswith("--"):
                    error("Error: --integrate requiere un código de seguridad.")
                    sys.exit(1)
                security_code = val
            else:
                error("Error: --integrate requiere un código de seguridad.")
                sys.exit(1)
        except ValueError:
            error("Error: --integrate requiere un código de seguridad.")
            sys.exit(1)

    # ==========================================================
    # ENTITY GENERATION / LOADING
    # ==========================================================

    header("AGENT IDENTITY")

    if not os.path.exists(IDENTITY_FILE) or regenerate:

        info("Generating new Agent identity...")

        agent_entity = EntityIdentity.generate(
            name="Agent"
        )

        agent_uid = (
            agent_entity.identification.uid
        )

        agent_pik = (
            agent_entity.cryptographic_identity.public_key
        )

        agent_ppik = (
            agent_entity.cryptographic_identity.private_key
        )

        with open(
            IDENTITY_FILE,
            "w"
        ) as f:

            json.dump(
                {
                    "uid": agent_uid,
                    "pik": agent_pik,
                    "ppik": agent_ppik
                },
                f,
                indent=4
            )

        success(
            "Agent identity generated and saved to disk"
        )

    else:

        info(
            "Loading existing Agent identity..."
        )

        with open(
            IDENTITY_FILE,
            "r"
        ) as f:

            identity_data = json.load(f)

            agent_uid = identity_data.get("uid")
            agent_pik = identity_data.get("pik")
            agent_ppik = identity_data.get("ppik")

        success(
            "Agent identity loaded successfully"
        )

    print(f"\nUID:\n{agent_uid}")
    print(f"\nPUBLIC KEY:\n{agent_pik}")
    print(f"\nPRIVATE KEY:\n{agent_ppik[:10]}")

    # ==========================================================
    # MANAGER DISCOVERY
    # ==========================================================

    header("MANAGER DISCOVERY")

    info(
        "Requesting manager logical identity..."
    )

    manager_uid_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{MANAGER_IDENTITY_LOGICAL}",
        json={
            "entity_uid": agent_uid,
            "public_key": agent_pik
        }
    )

    manager_uid = (
        manager_uid_request.json().get("uid")
    )

    info(
        "Requesting manager cryptographic identity..."
    )

    manager_pik_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{MANAGER_IDENTITY_PIK}"
    )

    manager_pik = (
        manager_pik_request.json().get(
            "public_key"
        )
    )

    manager_name = (
        manager_pik_request.json().get(
            "name"
        )
    )

    manager_fingerprint = (
        manager_pik_request.json().get(
            "fingerprint"
        )
    )

    info(
        "Requesting manager entity type..."
    )

    manager_type_request = requests.get(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{ENTITY_TYPE}"
    )

    manager_type = (
        manager_type_request.json().get("type")
    )

    success("Manager discovered")

    print(f"\nUID         : {manager_uid}")
    print(f"NAME        : {manager_name}")
    print(f"TYPE        : {manager_type}")
    print(f"FINGERPRINT : {manager_fingerprint}")

    print("\nPUBLIC KEY:\n")
    print(manager_pik)

    # ==========================================================
    # CLIENT AUTHENTICATION
    # ==========================================================

    header("CLIENT AUTHENTICATION")

    info(
        "Requesting authentication challenge..."
    )

    challenge_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_IDENTITY_AUTH_CHALLENGE}",
        json={
            "entity_uid": agent_uid,
            "public_key": agent_pik
        }
    )

    challenge = (
        challenge_request.json().get(
            "challenge"
        )
    )

    success("Challenge received")

    pretty(challenge)

    challenge_object = (
        ChallengeProtocol.challenge_from_dict(
            challenge
        )
    )

    info("Signing challenge...")

    signed_response = (
        ChallengeProtocol.sign(
            private_key=agent_ppik,
            challenge=challenge_object
        )
    )

    pretty(
        ChallengeProtocol.response_to_dict(
            signed_response
        )
    )

    info(
        "Submitting signed response..."
    )

    verify_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_IDENTITY_AUTH_VERIFY}",
        json={
            "challenge_id":
                challenge.get("challenge_id"),

            "response":
                ChallengeProtocol.response_to_dict(
                    signed_response
                ),

            "entity_uid": agent_uid,
            "public_key": agent_pik
        }
    )

    verification = verify_request.json()

    if verification.get("authenticated"):
        success("Authentication successful")
    else:
        error("Authentication failed")
        sys.exit(1)

    pretty(verification)

    auth_token = verification.get(
        "auth_token"
    )

    print("\nAUTH TOKEN:\n")
    print(auth_token)

    # ==========================================================
    # OPEN INTEGRATION
    # ==========================================================

    if integrate_mode:
        header("OPEN INTEGRATION")

        integration_request = requests.post(
            f"{SERVER_PROTOCOL.lower()}://"
            f"{SERVER_ADDRESS}:{SERVER_PORT}/"
            f"{CLIENT_INTEGRATION_OPEN}",
            headers={
                "Authorization":
                    f"Bearer {auth_token}"
            },
            json={
                "security_code": security_code,
                "entity_type": "AGENT"
            }
        )

        integration_result = (
            integration_request.json()
        )

        print()

        if integration_result.get("integrated"):
            success(
                "Agent integrated successfully"
            )
        else:
            error(
                "Agent integration failed"
            )

        pretty(integration_result)
        sys.exit(0)

    # ==========================================================
    # TUNNEL REQUEST
    # ==========================================================

    header("TUNNEL NEGOTIATION")

    info(
        "Requesting tunnel service..."
    )

    tunnel_request = requests.post(
        f"{SERVER_PROTOCOL.lower()}://"
        f"{SERVER_ADDRESS}:{SERVER_PORT}/"
        f"{CLIENT_TUNNEL_REQUEST}",
        json={
            "auth_token": auth_token
        }
    )

    tunnel_response = (
        tunnel_request.json()
    )

    authorized = (
        tunnel_response.get("ok")
    )

    tunnel_port = (
        tunnel_response.get("tunnel_port")
    )

    tunnel_token = (
        tunnel_response.get("tunnel_token")
    )

    if authorized:
        success("Tunnel granted")
    else:
        error("Tunnel denied")
        sys.exit(1)

    print(f"\nTunnel Token : {tunnel_token}")
    print(f"Tunnel Port  : {tunnel_port}")
    print(
        f"Tunnel Addr  : "
        f"{SERVER_ADDRESS}:{tunnel_port}"
    )

    # ==========================================================
    # READY
    # ==========================================================

    header("SESSION READY")

    success(
        "Agent integrated and operational"
    )

    print(
        f"\nTunnel endpoint:\n"
        f"{SERVER_ADDRESS}:{tunnel_port}\n"
    )

    communication = CommunicationHandler(
        auth_token=auth_token,
        tunnel_token=tunnel_token,
        tunnel_port=tunnel_port,
        tunnel_host=SERVER_ADDRESS
    )

    await communication.connect()

    #while True:
    #    print(f"Waiting...")
    #    time.sleep(100)

    shell_server = ShellServer(
        communication_handler=communication,
        auth_token=auth_token,
        tunnel_token=tunnel_token
    )

    await shell_server.start()


if __name__ == "__main__":
    asyncio.run(main())