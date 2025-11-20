from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Union

from .types import ColumnDef, ColumnType, Value

# --- Tokenizer -----------------------------------------------------------------

@dataclass(slots=True)
class Token:
    kind: str
    text: str

    def upper(self) -> str:
        return self.text.upper()

_TOKEN_REGEX = re.compile(
    r"""
    (?P<WS>\s+)|
    (?P<NUMBER>\d+)|
    (?P<STRING>'([^']*)')|
    (?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)|
    (?P<LPAREN>\()|
    (?P<RPAREN>\))|
    (?P<COMMA>,)|
    (?P<STAR>\*)|
    (?P<SEMICOLON>;)
    """,
    re.VERBOSE,
)

def tokenize(sql: str) -> List[Token]:
    tokens: List[Token] = []
    pos = 0
    while pos < len(sql):
        match = _TOKEN_REGEX.match(sql, pos)
        if not match:
            raise SyntaxError(f"Unexpected character at position {pos}: {sql[pos]!r}")
        kind = match.lastgroup
        text = match.group(0)
        pos = match.end()

        if kind == "WS":
            continue
        if kind == "STRING":
            # Strip the surrounding quotes
            inner = match.group(2)  # the ([^']*) group
            tokens.append(Token("STRING", inner))
        else:
            tokens.append(Token(kind, text))
    return tokens

# --- AST definitions -----------------------------------------------------------

@dataclass
class CreateTableStmt:
    name: str
    columns: List[ColumnDef]

@dataclass
class InsertStmt:
    table_name: str
    values: List[Value]

@dataclass
class SelectStmt:
    table_name: str
    columns: Optional[List[str]]  # None => *

Statement = Union[CreateTableStmt, InsertStmt, SelectStmt]

# --- Parser helpers ------------------------------------------------------------

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _match(self, kind: str, text_upper: Optional[str] = None) -> Token:
        tok = self._peek()
        if tok is None:
            raise SyntaxError(f"Expected {kind}, got end of input")
        if tok.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {tok.kind} ({tok.text!r})")
        if text_upper is not None and tok.upper() != text_upper:
            raise SyntaxError(f"Expected {text_upper}, got {tok.text!r}")
        self.pos += 1
        return tok

    def _match_keyword(self, keyword: str) -> Token:
        tok = self._peek()
        if tok is None or tok.kind != "IDENT" or tok.upper() != keyword:
            raise SyntaxError(f"Expected keyword {keyword}, got {tok.text if tok else 'EOF'}")
        self.pos += 1
        return tok

    def _optional(self, kind: str, text_upper: Optional[str] = None) -> Optional[Token]:
        tok = self._peek()
        if tok is None:
            return None
        if tok.kind != kind:
            return None
        if text_upper is not None and tok.upper() != text_upper:
            return None
        self.pos += 1
        return tok

    # --- Statement parsers -----------------------------------------------------

    def parse_statement(self) -> Statement:
        tok = self._peek()
        if tok is None:
            raise SyntaxError("Empty input")
        if tok.kind == "IDENT":
            upper = tok.upper()
            if upper == "CREATE":
                return self._parse_create_table()
            if upper == "INSERT":
                return self._parse_insert()
            if upper == "SELECT":
                return self._parse_select()
        raise SyntaxError(f"Unknown statement starting with {tok.text!r}")

    def _parse_create_table(self) -> CreateTableStmt:
        self._match_keyword("CREATE")
        self._match_keyword("TABLE")
        name_tok = self._match("IDENT")
        table_name = name_tok.text

        self._match("LPAREN")
        columns: List[ColumnDef] = []

        while True:
            col_name_tok = self._match("IDENT")
            type_tok = self._match("IDENT")
            col_def = ColumnDef(
                name=col_name_tok.text,
                col_type=ColumnType.from_sql(type_tok.text),
            )
            columns.append(col_def)

            if self._optional("COMMA") is not None:
                continue
            break

        self._match("RPAREN")
        # Optional trailing semicolon
        self._optional("SEMICOLON")
        return CreateTableStmt(name=table_name, columns=columns)

    def _parse_insert(self) -> InsertStmt:
        self._match_keyword("INSERT")
        self._match_keyword("INTO")
        table_tok = self._match("IDENT")
        table_name = table_tok.text

        self._match_keyword("VALUES")
        self._match("LPAREN")
        values: List[Value] = []

        while True:
            tok = self._peek()
            if tok is None:
                raise SyntaxError("Unexpected end of input in VALUES list")

            if tok.kind == "NUMBER":
                self.pos += 1
                values.append(int(tok.text))
            elif tok.kind == "STRING":
                self.pos += 1
                values.append(tok.text)
            else:
                raise SyntaxError(f"Expected NUMBER or STRING literal, got {tok.kind} ({tok.text!r})")

            if self._optional("COMMA") is not None:
                continue
            break

        self._match("RPAREN")
        self._optional("SEMICOLON")
        return InsertStmt(table_name=table_name, values=values)

    def _parse_select(self) -> SelectStmt:
        self._match_keyword("SELECT")
        columns: Optional[List[str]]

        tok = self._peek()
        if tok is None:
            raise SyntaxError("Unexpected end after SELECT")

        if tok.kind == "STAR":
            self.pos += 1
            columns = None
        else:
            cols: List[str] = []
            while True:
                ident_tok = self._match("IDENT")
                cols.append(ident_tok.text)
                if self._optional("COMMA") is not None:
                    continue
                break
            columns = cols

        self._match_keyword("FROM")
        table_tok = self._match("IDENT")
        table_name = table_tok.text

        self._optional("SEMICOLON")
        return SelectStmt(table_name=table_name, columns=columns)

def parse(sql: str) -> Statement:
    tokens = tokenize(sql)
    parser = Parser(tokens)
    stmt = parser.parse_statement()
    # Ensure no trailing junk
    if parser._peek() is not None:
        extra = parser._peek()
        raise SyntaxError(f"Unexpected token after statement: {extra.text!r}")
    return stmt
