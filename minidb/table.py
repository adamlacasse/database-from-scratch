from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Iterable, Optional

from .types import ColumnDef, Value

Row = Dict[str, Value]

@dataclass
class Table:
    name: str
    columns: List[ColumnDef]
    _rows: List[Row] = field(default_factory=list)

    @property
    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]

    def insert_row(self, values: List[Value]) -> None:
        if len(values) != len(self.columns):
            raise ValueError(
                f"Expected {len(self.columns)} values, got {len(values)}"
            )
        row: Row = {}
        for col, val in zip(self.columns, values):
            row[col.name] = val
        self._rows.append(row)

    def scan(self) -> Iterable[Row]:
        """Return an iterable over all rows (no filtering yet)."""
        return iter(self._rows)

    def select(
        self,
        column_names: Optional[List[str]] = None,
    ) -> List[Row]:
        """Return a list of rows; each row is a dict of column name -> value.

        If column_names is None, all columns are returned.
        """
        if column_names is None:
            return list(self.scan())

        missing = [c for c in column_names if c not in self.column_names]
        if missing:
            raise KeyError(f"Unknown columns in SELECT: {missing}")

        result: List[Row] = []
        for row in self.scan():
            projected = {col: row[col] for col in column_names}
            result.append(projected)
        return result
