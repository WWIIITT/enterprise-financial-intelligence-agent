import socket
from urllib.parse import urlparse


def can_open_tcp_connection(url: str, timeout_seconds: float = 0.2) -> bool:
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port
    if not host or not port:
        return False

    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False
