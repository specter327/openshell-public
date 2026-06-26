# Library import
from ..service import Subsystem
import fsresource_tree as fs
from configurations import Configurations, Setting
from datavalue import PrimitiveData

# Classes definition
class SettingsManager(Subsystem):
	SETTINGS_FILE: fs.File = fs.File(
		name="settings",
		extension="cfg"
	)
	BASE_CONFIGURATIONS: Configurations = Configurations()
	BASE_CONFIGURATIONS.add_setting(
		setting=Setting(
			value=PrimitiveData(
				data_type=str,
				value=None,
				name="Address",
				minimum_length=1,
				maximum_length=30,
				data_class=True
			),
			system_name="MANAGER_ADDRESS",
			symbolic_name="Manager Address",
			description="Manager Address: Domain name or public IPv4/IPv6",
			optional=False
		)
	)


	async def _initialize(self) -> bool:
		# Get the storage service
		storage_service = self.services.get("storage")

		# Regist the settings file
		try:
			storage_service.storage_schema.storage_tree.register(
				self.SETTINGS_FILE,
				parent=storage_service.storage_schema.DATA_ROOT
			)
		except fs.exceptions.ResourceAlreadyRegisteredError:
			pass

		return True

	async def _create_settings(self) -> bool:
		# Verify the current file existence
		if fs.operations.exists(self.SETTINGS_FILE): return True

		# Create the resource file
		return fs.operations.create(resource=self.SETTINGS_FILE)

	async def _update_settings(self, configurations: Configurations) -> bool:
		# Verify the current file existence
		if not fs.operations.exists(self.SETTINGS_FILE): return False

		# Open and write to the resource file
		file_handler = open(
			file=fs.operations.path(self.SETTINGS_FILE),
			mode='w',
			encoding="UTF-8"
		)

		file_handler.write(
			configurations.to_json()
		)

		# Close file
		file_handler.close()

		return True

	async def _load_settings(self) -> Configurations | bool:
		# Verify the current file existence
		if not fs.operations.exists(self.SETTINGS_FILE): return False

		# Open and read the settings file
		file_handler = open(
			file=fs.operations.path(self.SETTINGS_FILE),
			mode='r',
			encoding="UTF-8"
		)

		# Load the settings
		try:
			settings_structure = Configurations.from_json(
				text_content=file_handler.read()
			)
		except:
			return False

		# Close file
		file_handler.close()

		return settings_structure

	async def start(self) -> bool:

	    await self._initialize()

	    await self._create_settings()

	    loaded = await self._load_settings()

	    if not loaded:
		    await self._update_settings(
		    	configurations=self.BASE_CONFIGURATIONS
		    )

	    return True

	async def stop(self) -> bool:
		pass