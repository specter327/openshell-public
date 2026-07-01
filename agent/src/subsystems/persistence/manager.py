from pathlib import Path
import subprocess

from ..service import Subsystem

class PersistenceManager(Subsystem):

    SERVICE_NAME = "openshell-agent"

    @property
    def service_directory(self) -> Path:
        return (
            self.environment.home
            / ".config"
            / "systemd"
            / "user"
        )

    @property
    def service_path(self) -> Path:
        return (
            self.service_directory
            / f"{self.SERVICE_NAME}.service"
        )

    # =====================================================
    # INSTALL
    # =====================================================

    async def install(self,
        executable
    ) -> bool:

        storage_service = self.services.get("storage")
        program_path = storage_service.storage_schema.file_system.operations.path(executable)

        self.service_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        service = f"""
[Unit]
Description=OpenShell Agent
After=network-online.target

[Service]
Type=simple
ExecStart={program_path}
Restart=always
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=5

[Install]
WantedBy=default.target
""".strip()

        self.service_path.write_text(
            service
        )

        subprocess.run(
            [
                "systemctl",
                "--user",
                "daemon-reload"
            ],
            check=True
        )

        return True

    # =====================================================
    # UNINSTALL
    # =====================================================

    async def uninstall(self) -> bool:

        await self.disable()

        if self.service_path.exists():
            self.service_path.unlink()

        subprocess.run(
            [
                "systemctl",
                "--user",
                "daemon-reload"
            ],
            check=True
        )

        return True

    # =====================================================
    # ENABLE
    # =====================================================

    async def enable(self) -> bool:

        subprocess.run(
            [
                "systemctl",
                "--user",
                "enable",
                "--now",
                self.SERVICE_NAME
            ],
            check=True
        )

        return True

    # =====================================================
    # DISABLE
    # =====================================================

    async def disable(self) -> bool:

        subprocess.run(
            [
                "systemctl",
                "--user",
                "disable",
                "--now",
                self.SERVICE_NAME
            ],
            check=False
        )

        return True

    # =====================================================
    # STATUS
    # =====================================================

    async def status(self) -> dict:

        exists = self.service_path.exists()

        active = subprocess.run(
            [
                "systemctl",
                "--user",
                "is-active",
                self.SERVICE_NAME
            ],
            capture_output=True,
            text=True
        )

        enabled = subprocess.run(
            [
                "systemctl",
                "--user",
                "is-enabled",
                self.SERVICE_NAME
            ],
            capture_output=True,
            text=True
        )

        return {

            "installed": exists,

            "active":
                active.stdout.strip() == "active",

            "enabled":
                enabled.stdout.strip() == "enabled"
        }