"""Cortex - Archive Tool
Create, list, and extract zip archives using the Python standard library.
"""
from __future__ import annotations

import os
import zipfile
from pathlib import Path

from tools import BaseTool


def _safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    target_root = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if target_root not in (target, *target.parents):
            raise ValueError(f"unsafe archive member: {member.filename}")
    archive.extractall(destination)


class ArchiveTool(BaseTool):
    name = "archive"
    description = "Create, list, and extract zip archives. Commands: create <zip> | <path> [path...] ; list <zip> ; extract <zip> | <dest>."
    usage_example = "archive create project.zip | README.md tools"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[archive] Commands: create <zip> | <path> [path...] ; list <zip> ; extract <zip> | <dest>"

        try:
            command, _, rest = raw.partition(" ")
            command = command.lower()
            rest = rest.strip()

            if command == "create":
                archive_part, sep, sources_part = rest.partition("|")
                if not sep:
                    return "[archive] Usage: create <archive.zip> | <path> [path...]"
                archive_path = Path(archive_part.strip()).expanduser()
                sources = [Path(p).expanduser() for p in sources_part.split() if p.strip()]
                if not sources:
                    return "[archive] Provide at least one source path."
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                added = 0
                with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    for source in sources:
                        if not source.exists():
                            return f"[archive] Source not found: {source}"
                        if source.is_file():
                            archive.write(source, source.name)
                            added += 1
                        else:
                            base = source.parent
                            for path in source.rglob("*"):
                                if path.is_file():
                                    archive.write(path, path.relative_to(base))
                                    added += 1
                return f"[archive] Created {archive_path} with {added} file(s)."

            if command == "list":
                archive_path = Path(rest).expanduser()
                if not archive_path.is_file():
                    return f"[archive] File not found: {archive_path}"
                with zipfile.ZipFile(archive_path) as archive:
                    names = archive.namelist()
                lines = [f"[archive list: {archive_path}] {len(names)} item(s)"]
                lines.extend(f"  {name}" for name in names[:50])
                if len(names) > 50:
                    lines.append(f"  ... and {len(names) - 50} more")
                return "\n".join(lines)

            if command == "extract":
                archive_part, sep, dest_part = rest.partition("|")
                if not sep:
                    return "[archive] Usage: extract <archive.zip> | <destination>"
                archive_path = Path(archive_part.strip()).expanduser()
                destination = Path(dest_part.strip()).expanduser()
                if not archive_path.is_file():
                    return f"[archive] File not found: {archive_path}"
                destination.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(archive_path) as archive:
                    count = len(archive.infolist())
                    _safe_extract(archive, destination)
                return f"[archive] Extracted {count} item(s) to {destination}."

            return f"[archive] Unknown command: {command}"
        except Exception as exc:
            return f"[archive] ERROR: {exc}"
