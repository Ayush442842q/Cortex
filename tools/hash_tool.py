"""Cortex - Hash Tool
Generate file checksums and text hashes using the Python standard library.
"""
from __future__ import annotations

import hashlib
import hmac
import os

from tools import BaseTool


ALGORITHMS = {
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "blake2b",
    "blake2s",
}


def _hash_bytes(data: bytes, algorithm: str) -> str:
    if algorithm not in ALGORITHMS:
        raise ValueError(f"unknown algorithm '{algorithm}'")
    digest = hashlib.new(algorithm)
    digest.update(data)
    return digest.hexdigest()


def _hash_file(path: str, algorithm: str) -> str:
    if algorithm not in ALGORITHMS:
        raise ValueError(f"unknown algorithm '{algorithm}'")
    digest = hashlib.new(algorithm)
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class HashTool(BaseTool):
    name = "hash"
    description = "Create checksums for text or files and verify expected digests. Commands: text, file, verify, algorithms."
    usage_example = "hash file sha256 README.md"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[hash] Commands: text <algo> <text> | file <algo> <path> | verify <algo> <path> <expected> | algorithms"

        parts = raw.split(None, 2)
        command = parts[0].lower()

        try:
            if command == "algorithms":
                return "[hash algorithms]\n" + "\n".join(f"  {name}" for name in sorted(ALGORITHMS))

            if command == "text":
                if len(parts) < 3:
                    return "[hash] Usage: text <algorithm> <text>"
                algorithm, text = parts[1].lower(), parts[2]
                return f"{algorithm}: {_hash_bytes(text.encode('utf-8'), algorithm)}"

            if command == "file":
                if len(parts) < 3:
                    return "[hash] Usage: file <algorithm> <path>"
                algorithm, path = parts[1].lower(), os.path.expanduser(parts[2])
                if not os.path.isfile(path):
                    return f"[hash] File not found: {path}"
                return f"{algorithm}: {_hash_file(path, algorithm)}  {path}"

            if command == "verify":
                verify_parts = raw.split(None, 3)
                if len(verify_parts) < 4:
                    return "[hash] Usage: verify <algorithm> <path> <expected_digest>"
                algorithm = verify_parts[1].lower()
                path_and_expected = verify_parts[2:]
                path, expected = path_and_expected[0], path_and_expected[1].strip().lower()
                path = os.path.expanduser(path)
                if not os.path.isfile(path):
                    return f"[hash] File not found: {path}"
                actual = _hash_file(path, algorithm)
                ok = hmac.compare_digest(actual.lower(), expected)
                return f"[hash verify] {'OK' if ok else 'MISMATCH'}\nactual:   {actual}\nexpected: {expected}"

            return f"[hash] Unknown command: {command}"
        except Exception as exc:
            return f"[hash] ERROR: {exc}"
