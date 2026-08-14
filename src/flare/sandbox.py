#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import os.path
import platform
import subprocess
from pathlib import Path
from typing import List


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

    def _launch_mac_os(self, args: List[str]):
        seatbelt_profile_directory = (
            self.project_directory / "src" / "sandbox" / "macos"
        )
        seatbelt_profile: str

        # We set the content of `main.sb` first because the `main.sb` file
        # includes the needed "version" declaration, which must occur at the
        # very beginning of the Seatbelt profile.

        with open(str(seatbelt_profile_directory / "main.sb"), "r") as f:
            seatbelt_profile = f.read()

        for file in seatbelt_profile_directory.glob("*.sb"):
            # we have already added `main.sb`
            if file.name == "main.sb":
                continue

            # add some padding before the new profile gets added
            # to make life easier for the Seatbelt parser.
            seatbelt_profile += "\n\n"

            with open(file, "r") as f:
                seatbelt_profile += f.read()

        subprocess.run(
            [
                "sandbox-exec",
                "-p",
                seatbelt_profile,
                "-D",
                f"PROJ_DIR={str(self.project_directory)}",
                str(self.target),
                *args,
            ]
        )

    def launch(self, args: List[str]):
        match platform.system():
            case "Darwin":
                self._launch_mac_os(args)
            case _:
                raise SandboxError("Operating system not supported for sandboxing!")
