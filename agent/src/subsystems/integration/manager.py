# Library import
from ..service import Subsystem
import fsresource_tree as fs
import json

# Classes definition
class IntegrationManager(Subsystem):
	pass

	async def start(self) -> bool:
		# Get the bootstrap service
		self._bootstrap_service = self.services.get("bootstrap")

		# Search the: passports, bootstrap file
		bootstrap_passports_file = await self._bootstrap_service.get("passports")
		bootstrap_passports_file_path = fs.operations.path(bootstrap_passports_file)

		print(f"[INTEGRATION-MANAGER] Bootstrap passports file: {bootstrap_passports_file_path}")

		# Extract passports data
		if not bootstrap_passports_file: return False

		with open(
			file=bootstrap_passports_file_path,
			mode='r',
			encoding="UTF-8"
		) as file:
			try:
				passports = json.loads(file.read())
			except:
				passports = None
			
			print(f"[INTEGRATION-MANAGER] Passports content: {file.read()}")

		if not passports:
			return False

		# Execute integration
		self._manager_service = self.services.get("manager")

		for passport in passports.get('passports', {}):
			print(f"Passport:")
			print(passport)
			print(f"Security code: {passport.get('security_code')}")

			await self._manager_service.open_integration(
				auth_token=self.runtime.auth_token,
				security_code=passport.get("security_code"),
				entity_type="AGENT"
			)


		# Return results
		return True

	async def stop(self) -> bool:
		return True