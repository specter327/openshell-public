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
    Runtime execution environment.

    This object centralizes every property related to the
    current execution context.

    Responsibilities

        - Detect development / packaged execution
        - Detect PyInstaller environment
        - Resolve execution command
        - Resolve entrypoint
        - Resolve interpreter
        - Resolve bundle paths
        - Resolve working directory
        - Provide platform information
    """

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

    @property
    def arguments(self) -> list[str]:
        """
        Original process arguments.
        """
        return list(sys.argv)

    # ======================================================
    # EXECUTION
    # ======================================================

    @property
    def interpreter(self) -> Path | None:
        """
        Python interpreter.

        Development:
            /usr/bin/python3
            venv/bin/python

        Frozen:
            None
        """

        if self.frozen:
            return None

        return Path(sys.executable).resolve()

    @property
    def entrypoint(self) -> Path:
        """
        OpenShell entrypoint.

        Development:
            Entry script.

        Frozen:
            Executable itself.
        """

        if self.frozen:
            return Path(sys.executable).resolve()

        return Path(sys.argv[0]).resolve()

    @property
    def command(self) -> list[str]:
        """
        Command required to execute OpenShell.

        Development:
            [
                python,
                main.py
            ]

        Frozen:
            [
                agent
            ]
        """

        if self.frozen:

            return [
                str(self.entrypoint)
            ]

        return [
            str(self.interpreter),
            str(self.entrypoint)
        ]

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
    def executable_directory(self) -> Path:
        """
        Directory containing the OpenShell entrypoint.
        """
        return self.entrypoint.parent

    @property
    def script(self) -> Path:
        """
        Alias of entrypoint.
        """
        return self.entrypoint

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
            executable directory.
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
        return Path(
            os.getenv(
                "TMPDIR",
                "/tmp"
            )
        ).resolve()

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

            "arguments": self.arguments,

            "cwd": str(self.cwd),

            "interpreter":
                None if self.interpreter is None
                else str(self.interpreter),

            "entrypoint":
                str(self.entrypoint),

            "command":
                self.command,

            "script":
                str(self.script),

            "script_directory":
                str(self.script_directory),

            "bundle_root":
                str(self.bundle_root),

            "executable_directory":
                str(self.executable_directory),

            "home":
                str(self.home),

            "temp":
                str(self.temp),

            "system":
                self.system,

            "release":
                self.release,

            "machine":
                self.machine,

            "architecture":
                self.architecture,

            "python_version":
                self.python_version,

            "hostname":
                self.hostname
        }