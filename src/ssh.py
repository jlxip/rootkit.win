"""Server, SSH-wise"""

import paramiko


class SshServerInterface(paramiko.ServerInterface):
    """SSH Server configuration"""

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.common.OPEN_SUCCEEDED
        return paramiko.common.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def check_channel_pty_request(
        self,
        channel: paramiko.Channel,
        term: bytes,
        width: int,
        height: int,
        pixelwidth: int,
        pixelheight: int,
        modes: bytes,
    ) -> bool:
        return True

    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        return True

    def check_auth_none(self, username: str) -> int:
        return paramiko.common.AUTH_SUCCESSFUL
