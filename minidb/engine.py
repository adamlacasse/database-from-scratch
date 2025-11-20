from __future__ import annotations

from typing import Any, List, Optional

from .database import Database
from .parser import (
    Statement,
    CreateTableStmt,
    InsertStmt,
    SelectStmt,
)
from .table import Row
from .types import ColumnDef

class Engine:
    """Executes parsed SQL statements against a Database."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def execute(self, stmt: Statement) -> Optional[List[Row]]:
        if isinstance(stmt, CreateTableStmt):
            return self._exec_create_table(stmt)
        if isinstance(stmt, InsertStmt):
            return self._exec_insert(stmt)
        if isinstance(stmt, SelectStmt):
            return self._exec_select(stmt)
        raise TypeError(f"Unsupported statement type: {type(stmt)!r}")

    # --- Handlers -------------------------------------------------------------

    def _exec_create_table(self, stmt: CreateTableStmt) -> None:
        self.db.create_table(stmt.name, stmt.columns)
        return None

    def _exec_insert(self, stmt: InsertStmt) -> None:
        self.db.insert(stmt.table_name, stmt.values)
        return None

    def _exec_select(self, stmt: SelectStmt) -> List[Row]:
        return self.db.select(stmt.table_name, stmt.columns)
