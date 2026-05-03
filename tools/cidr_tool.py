"""Cortex - CIDR Tool."""
from __future__ import annotations

import ipaddress
from tools import BaseTool


class CidrTool(BaseTool):
    name = "cidr"
    description = "Inspect an IPv4/IPv6 CIDR network."
    usage_example = "cidr 192.168.1.0/24"

    def run(self, input: str) -> str:
        try:
            net = ipaddress.ip_network(input.strip(), strict=False)
            return f"network: {net.network_address}\nbroadcast: {net.broadcast_address}\nversion: IPv{net.version}\naddresses: {net.num_addresses}"
        except ValueError as exc:
            return f"[cidr] ERROR: {exc}"
