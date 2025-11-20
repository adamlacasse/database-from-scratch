from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union, Any

class ColumnType(str, Enum):
    INT = "INT"
    TEXT = "TEXT"
    BOOL = "BOOL"

    @classmethod
    def from_sql(cls, type_name: str) -> "ColumnType":
        upper = type_name.upper()
        try:
            return cls[upper]
        except KeyError:
            raise ValueError(f"Unsupported column type: {type_name!r}") from None


Value = Union[int, str, bool, None]


@dataclass(slots=True)
class ColumnDef:
    name: str
    col_type: ColumnType
    nullable: bool = True
    primary_key: bool = False
