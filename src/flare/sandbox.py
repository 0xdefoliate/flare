#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import os.path
import platform
import subprocess
import sys
from pathlib import Path
from typing import List

from flare.sandbox_policy.macos import POLICY_MAC_OS


class SandboxError(Exception):
    def __init__(self, message: str):
        super().__init__(f"SandboxError: {message}")


class Sandbox:
    """Performs sandboxing operations on a given target."""

    target: Path
    """ The script/executable to be confined (sandboxed) """

    project_directory: Path
    """ This project's root directory """

    def __init__(self, target: Path):
        self.target = target

        # Probably not the brightest idea to assume this file is always inside `src/flare`.
        # This will be changed in the future.
        self.project_directory = Path(os.path.dirname(__file__)).parent.parent
        print(str(self.project_directory))

    def _launch_mac_os(self, args: List[str]):
        sandbox_env = {
            "PATH": os.environ.get("PATH", ""),
            "LANG": "C.UTF-8",
            "TERM": os.environ.get("TERM", ""),
            "COLORTERM": os.environ.get("COLORTERM", "")
        }

        subprocess.run(
            [
                "sandbox-exec",
                "-p",
                POLICY_MAC_OS,
                "-D",
                f"PROJ_DIR={str(self.project_directory)}",
                sys.executable,
                str(self.target),
                *args,
            ],
            env=sandbox_env,
        )

    def launch(self, args: List[str]):
        match platform.system():
            case "Darwin":
                self._launch_mac_os(args)
            case _:
                raise SandboxError("Operating system not supported for sandboxing!")
