from __future__ import annotations

import sys
from typing import Iterable, Mapping, Any, List

from minidb.database import Database
from minidb.engine import Engine
from minidb.parser import parse
from minidb.table import Row

def format_rows(rows: List[Row]) -> str:
    if not rows:
        return "(0 rows)"

    # Get the union of all keys (columns) in order of first appearance
    cols: List[str] = []
    for row in rows:
        for k in row.keys():
            if k not in cols:
                cols.append(k)

    # Compute column widths
    def cell_str(v: Any) -> str:
        return "" if v is None else str(v)

    col_widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            col_widths[c] = max(col_widths[c], len(cell_str(row.get(c))))

    # Header
    header = " | ".join(c.ljust(col_widths[c]) for c in cols)
    sep = "-+-".join("-" * col_widths[c] for c in cols)
    lines = [header, sep]

    # Rows
    for row in rows:
        line = " | ".join(cell_str(row.get(c)).ljust(col_widths[c]) for c in cols)
        lines.append(line)

    lines.append(f"({len(rows)} rows)")
    return "\n".join(lines)

def repl() -> None:
    db = Database()
    engine = Engine(db)

    print("MiniDB - tiny educational database")
    print("Type SQL and end with ';'. Ctrl-D to exit.")
    buffer = ""

    while True:
        try:
            prompt = "MiniDB> " if not buffer else "    ...> "
            line = input(prompt)
        except EOFError:
            print()
            break

        buffer += line.strip() + " "
        if ";" not in buffer:
            continue

        # Support only one statement at a time for now
        sql = buffer.strip()
        buffer = ""

        try:
            stmt = parse(sql)
            result = engine.execute(stmt)
            if result is None:
                print("OK")
            else:
                print(format_rows(result))
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}")

if __name__ == "__main__":
    repl()
