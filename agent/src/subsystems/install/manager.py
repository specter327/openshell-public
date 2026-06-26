# Library import
from ..service import Subsystem
import fsresource_tree as fs

# Classes definition
class InstallationManager(Subsystem):
	INSTALL_FLAG: fs.File = fs.File(
		name="installed",
		extension="flag"
	)

	async def install(self) -> bool:
		# Get the storage service
		storage_service = self.core.services.get("storage")

		# Verify current installation
		if await self.is_installed(): return True

		storage_service.storage_schema.file_system.operations.create(
			resource=self.INSTALL_FLAG,
			recursive_parent=True
		)

		print(f"[INSTALL-MANAGER] Flag file successfully created")
		print(storage_service.storage_schema.file_system.renderers.mermaid(storage_service.storage_schema.UNIT_ROOT))

		return True

	async def uninstall(self) -> bool:
		# Get the storage service
		storage_service = self.core.services.get("storage")

		# Delete the agent structure
		print(f"[INSTALL-MANAGER] Deleting: {storage_service.storage_schema.file_system.operations.path(storage_service.storage_schema.AGENT_ROOT)}...")
		storage_service.storage_schema.file_system.operations.delete(
			resource=storage_service.storage_schema.AGENT_ROOT,
			recursive_children=True
		)

		print(f"[INSTALL-MANAGER] Directory successfully deleted")

		return True

	async def is_installed(self) -> bool:
		# Get the storage service
		storage_service = self.core.services.get("storage")

		# Register installation flag file
		if not storage_service.storage_schema.storage_tree.registered(
			resource=self.INSTALL_FLAG
		):
			print(f"[INSTALL-MANAGER] Unregistered flag file")
			storage_service.storage_schema.storage_tree.register(
				resource=self.INSTALL_FLAG,
				parent=storage_service.storage_schema.DATA_ROOT
			)
			print(f"[INSTALL-MANAGER] Flag file successfully registered")
		else:
			print(f"[INSTALL-MANAGER] Flag file already registered")

		# Verify the installation flag file
		if storage_service.storage_schema.file_system.operations.exists(resource=self.INSTALL_FLAG):
			print("[INSTALL-MANAGER] Install flag currently created")
			return True
		else:
			print("[INSTALL-MANAGER] Install flag unexistent")
			return False