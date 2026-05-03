"""Cortex - IP Info Tool."""
from __future__ import annotations

import ipaddress
from tools import BaseTool


class IpInfoTool(BaseTool):
    name = "ip_info"
    description = "Inspect whether an IP address is private, global, loopback, multicast, or reserved."
    usage_example = "ip_info 8.8.8.8"

    def run(self, input: str) -> str:
        try:
            ip = ipaddress.ip_address(input.strip())
            return f"version: IPv{ip.version}\nprivate: {ip.is_private}\nglobal: {ip.is_global}\nloopback: {ip.is_loopback}\nmulticast: {ip.is_multicast}\nreserved: {ip.is_reserved}"
        except ValueError as exc:
            return f"[ip_info] ERROR: {exc}"
