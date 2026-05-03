"""Cortex - SQLite Tool
Inspect and query SQLite databases using the Python standard library.
"""
from __future__ import annotations

import json
import os
import sqlite3

from tools import BaseTool


READONLY_PREFIXES = ("select", "pragma", "with", "explain")


def _connect(path: str) -> sqlite3.Connection:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


class SQLiteTool(BaseTool):
    name = "sqlite"
    description = "Inspect and query SQLite databases read-only. Commands: tables <db>, schema <db> [table], query <db> | <select sql>, count <db> <table>."
    usage_example = "sqlite tables app.db"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[sqlite] Commands: tables <db> | schema <db> [table] | query <db> | <select sql> | count <db> <table>"

        command, _, rest = raw.partition(" ")
        command = command.lower()
        rest = rest.strip()

        try:
            if command == "tables":
                if not rest:
                    return "[sqlite] Usage: tables <db>"
                with _connect(os.path.expanduser(rest)) as conn:
                    rows = conn.execute(
                        "select name, type from sqlite_master where type in ('table', 'view') order by type, name"
                    ).fetchall()
                    if not rows:
                        return "[sqlite] No tables or views found."
                    return "[sqlite tables]\n" + "\n".join(f"  {row['type']}: {row['name']}" for row in rows)

            if command == "schema":
                parts = rest.split(None, 1)
                if not parts:
                    return "[sqlite] Usage: schema <db> [table]"
                db_path = os.path.expanduser(parts[0])
                table = parts[1].strip() if len(parts) > 1 else ""
                with _connect(db_path) as conn:
                    if table:
                        rows = conn.execute(
                            "select sql from sqlite_master where name = ? and sql is not null",
                            (table,),
                        ).fetchall()
                    else:
                        rows = conn.execute(
                            "select sql from sqlite_master where sql is not null order by type, name"
                        ).fetchall()
                    if not rows:
                        return f"[sqlite] No schema found{f' for {table}' if table else ''}."
                    return "[sqlite schema]\n" + "\n\n".join(row["sql"] for row in rows)

            if command == "query":
                db_part, sep, sql = rest.partition("|")
                if not sep:
                    return "[sqlite] Usage: query <db> | <select sql>"
                db_path = os.path.expanduser(db_part.strip())
                sql = sql.strip()
                if not sql.lower().startswith(READONLY_PREFIXES):
                    return "[sqlite] Only read-only SELECT/PRAGMA/WITH/EXPLAIN queries are allowed."
                with _connect(db_path) as conn:
                    rows = conn.execute(sql).fetchmany(50)
                    return json.dumps([dict(row) for row in rows], indent=2, default=str)

            if command == "count":
                parts = rest.split()
                if len(parts) != 2:
                    return "[sqlite] Usage: count <db> <table>"
                db_path, table = os.path.expanduser(parts[0]), parts[1]
                safe_table = '"' + table.replace('"', '""') + '"'
                with _connect(db_path) as conn:
                    count = conn.execute(f"select count(*) as n from {safe_table}").fetchone()["n"]
                return f"{table}: {count} row(s)"

            return f"[sqlite] Unknown command: {command}"
        except Exception as exc:
            return f"[sqlite] ERROR: {exc}"
