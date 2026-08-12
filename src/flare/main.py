import os
import subprocess
import platform

from pathlib import Path

from flare.renderer import renderer
from flare.sandbox import SEATBELT_PROFILE

def main() -> None:
    script_dir = Path(os.path.dirname(__file__))
    entrypoint_path = script_dir / "renderer" / "renderer.py"

    if platform.system() == 'Darwin':
        subprocess.run([
            "sandbox-exec",
            "-p",
            SEATBELT_PROFILE,
            "-D",
            f"ENTRYPOINT={str(entrypoint_path)}",
            str(entrypoint_path)
        ])
    else:
        print("You are running this program unsandboxed which may decrease security somewhat.")
        print()
        print("Sandboxing is currently only supported on macOS, so please contribute if you want")
        print("other platforms to be supported as well.")

        renderer.renderer()

