import ipaddress
import socket
from urllib.parse import urlparse

PRIVATE_NETS = (
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
)


class URLValidationError(ValueError):
    pass


def validate_public_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise URLValidationError("Only http and https URLs are allowed")
    if not parsed.hostname:
        raise URLValidationError("URL is missing a hostname")

    host = parsed.hostname.lower()
    if host in {"localhost", "0.0.0.0"}:
        raise URLValidationError("Localhost targets are blocked")

    try:
        addr_infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise URLValidationError(f"Host resolution failed: {host}") from exc

    for info in addr_infos:
        ip = ipaddress.ip_address(info[4][0])
        if any(ip in net for net in PRIVATE_NETS):
            raise URLValidationError(f"Private/internal target blocked: {ip}")

    return url
