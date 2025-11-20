from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .table import Table, Row
from .types import ColumnDef

@dataclass
class Database:
    tables: Dict[str, Table] = field(default_factory=dict)

    def create_table(self, name: str, columns: List[ColumnDef]) -> None:
        key = name.lower()
        if key in self.tables:
            raise ValueError(f"Table {name!r} already exists")
        self.tables[key] = Table(name=name, columns=columns)

    def get_table(self, name: str) -> Table:
        key = name.lower()
        try:
            return self.tables[key]
        except KeyError:
            raise KeyError(f"Table {name!r} does not exist") from None

    def insert(self, table_name: str, values: List[object]) -> None:
        table = self.get_table(table_name)
        table.insert_row(values)

    def select(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
    ) -> List[Row]:
        table = self.get_table(table_name)
        return table.select(columns)
