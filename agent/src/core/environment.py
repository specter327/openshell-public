# ==========================================================
# OpenShell Agent
# Runtime Environment
# ==========================================================

from pathlib import Path
import platform
import sys
import os


class RuntimeEnvironment:
    """
    Execution environment information.

    This object centralizes every property related to the
    current execution context.

    Responsibilities:

        - Detect development / frozen execution
        - Detect PyInstaller environment
        - Resolve executable paths
        - Resolve bundle paths
        - Resolve working directory
        - Provide platform information

    It does NOT contain:

        - Business logic
        - Storage logic
        - Installation logic
        - Persistence logic
    """

    def __init__(self):
        pass

    # ======================================================
    # EXECUTION MODE
    # ======================================================

    @property
    def frozen(self) -> bool:
        """
        Running from a packaged executable.
        """
        return getattr(sys, "frozen", False)

    @property
    def arguments(self) -> list:
        return sys.argv
    
    @property
    def development(self) -> bool:
        """
        Running directly from source code.
        """
        return not self.frozen

    @property
    def pyinstaller(self) -> bool:
        """
        Running under PyInstaller.
        """
        return hasattr(sys, "_MEIPASS")

    # ======================================================
    # PATHS
    # ======================================================

    @property
    def cwd(self) -> Path:
        """
        Current working directory.
        """
        return Path.cwd().resolve()

    @property
    def executable(self) -> Path:
        """
        Executable currently running.

        Development:
            python executable

        Frozen:
            packaged executable
        """
        return Path(sys.executable).resolve()

    @property
    def executable_directory(self) -> Path:
        """
        Directory containing the executable.
        """
        return self.executable.parent

    @property
    def script(self) -> Path:
        """
        Current entry script.

        Development:
            agent

        Frozen:
            executable itself
        """
        return Path(sys.argv[0]).resolve()

    @property
    def script_directory(self) -> Path:
        return self.script.parent

    @property
    def bundle_root(self) -> Path:
        """
        Runtime bundle root.

        Development:
            Current working directory.

        PyInstaller (--onefile):
            sys._MEIPASS

        Frozen (--onedir):
            executable directory
        """

        if self.pyinstaller:
            return Path(sys._MEIPASS).resolve()

        if self.frozen:
            return self.executable_directory

        return self.cwd

    # ======================================================
    # USER
    # ======================================================

    @property
    def home(self) -> Path:
        return Path.home()

    @property
    def temp(self) -> Path:
        return Path(os.getenv("TMPDIR", "/tmp")).resolve()

    # ======================================================
    # PLATFORM
    # ======================================================

    @property
    def system(self) -> str:
        return platform.system()

    @property
    def release(self) -> str:
        return platform.release()

    @property
    def machine(self) -> str:
        return platform.machine()

    @property
    def architecture(self) -> str:
        return platform.architecture()[0]

    @property
    def python_version(self) -> str:
        return platform.python_version()

    @property
    def hostname(self) -> str:
        return platform.node()

    # ======================================================
    # EXPORT
    # ======================================================

    def to_dict(self) -> dict:

        return {

            "development": self.development,

            "frozen": self.frozen,

            "pyinstaller": self.pyinstaller,

            "cwd": str(self.cwd),

            "script": str(self.script),

            "script_directory": str(
                self.script_directory
            ),

            "bundle_root": str(
                self.bundle_root
            ),

            "executable": str(
                self.executable
            ),

            "executable_directory": str(
                self.executable_directory
            ),

            "home": str(self.home),

            "temp": str(self.temp),

            "system": self.system,

            "release": self.release,

            "machine": self.machine,

            "architecture": self.architecture,

            "python_version": self.python_version,

            "hostname": self.hostname
        }