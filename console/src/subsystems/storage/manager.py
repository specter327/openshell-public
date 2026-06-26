# Library import
from ..service import Subsystem
import fsresource_tree as fs
import getpass

# Classes definition
class StorageSchemaLinux:
	def __init__(self):
		self.file_system = fs
		
		# Storage structure definition
		self.storage_tree = fs.ResourceTree(
			name="Storage System",
			description="GNU/Linux Storage System"
		)

		# Resources definition and registration
		## Directories
		self.UNIT_ROOT = fs.Directory(name="/"); self.storage_tree.register(self.UNIT_ROOT)
		self.HOME_ROOT = fs.Directory(name="home"); self.storage_tree.register(self.HOME_ROOT, parent=self.UNIT_ROOT)
		self.USER_DIR = fs.Directory(name=getpass.getuser()); self.storage_tree.register(self.USER_DIR, parent=self.HOME_ROOT)
		self.AGENT_ROOT = fs.Directory(name=".osac"); self.storage_tree.register(self.AGENT_ROOT, parent=self.USER_DIR)
		self.DATA_ROOT = fs.Directory(name="data"); self.storage_tree.register(self.DATA_ROOT, parent=self.AGENT_ROOT)
		self.SOFTWARE_ROOT = fs.Directory(name="software"); self.storage_tree.register(self.SOFTWARE_ROOT, parent=self.AGENT_ROOT)

		## Files
		pass


class StorageManager(Subsystem):
	def __init__(
		self,
		core
	):
		super().__init__(core)

		self.storage_schema: StorageSchema = None

	async def start(self):
		# Adaptabilidad segun sistema operativo
		self.storage_schema = StorageSchemaLinux()

	async def stop(self): pass

class StorageRuntime:
	pass