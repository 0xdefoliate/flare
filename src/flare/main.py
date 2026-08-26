#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import os
import subprocess
import sys
from pathlib import Path

from flare.sandbox import Sandbox, SandboxError


def main() -> None:
    args = sys.argv[1:]
    target = Path(os.path.dirname(__file__)) / "renderer.py"

    sandbox = Sandbox(target)

    try:
        sandbox.launch(args)
    except SandboxError:
        print("It seems like Flare doesn't support sandboxing your platform yet...")
        print("Would you still like to use it, despite increased security risks?")
        reply = input("type 'YES' to run unsandboxed: ")

        if reply != "YES":
            return sys.exit(0)

        subprocess.run([str(target), *args])
