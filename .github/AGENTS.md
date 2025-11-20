# MiniDB Agent Guide

## Snapshot & workflows
- Python 3.11 project (`pyproject.toml`) with zero runtime deps; `pytest` is optional via the `dev` extra but no test suite exists yet.
- Entry point is `main.py`, which hosts the REPL. Run the project with `python main.py`; mirror these commands in `README.md` if you change them.
- `README.md` is the public-facing spec (feature checklist, SQL surface, run instructions). Update it whenever you expand SQL syntax or add modules so future agents have a single source of truth.

## Layout primer
- `minidb/parser.py` tokenizes SQL via a regex, builds a tiny AST (`CreateTableStmt`, `InsertStmt`, `SelectStmt`). Extend the SQL grammar here first; keep tokenizer + AST additions in sync.
- `minidb/engine.py` is the dispatcher: it receives parsed statements and calls the matching handler (`_exec_create_table`, `_exec_insert`, `_exec_select`). New verbs belong here.
- `minidb/database.py` manages table registration and delegates row work to `Table` objects. It is the right place for catalog-wide checks (duplicates, table existence).
- `minidb/table.py` stores rows as in-memory dicts and handles projection. If you add WHERE clauses or indexes, start by extending `Table.select`/`scan`.
- `minidb/types.py` defines `ColumnType`, `ColumnDef`, and the `Value` alias. Update this when introducing new SQL types or column attributes.
- `.github/copilot-instructions.md` captures collaboration expectations; keep AGENTS.md aligned with it whenever workflows shift.

## Data flow (SQL ➜ result)
1. `main.py` REPL reads a full statement (terminated by `;`) and passes it to `parse`.
2. `Parser.parse_statement` builds an AST and enforces trailing-token checks.
3. `Engine.execute` pattern-matches the AST node and calls the corresponding `_exec_*` method.
4. `Database` + `Table` mutate or read the in-memory store, returning a list of row dicts.
5. `main.format_rows` renders the result set for the console.

## Extending safely
- Keep SQL keywords uppercase in parser errors for clarity, but accept case-insensitive identifiers (the tokenizer uppercases for comparisons).
- Respect the invariant that `Table.insert_row` receives values matching the number/order of `ColumnDef`s; validate inputs at the engine layer before they reach the table if you add optional column lists.
- Document every new statement (syntax example + sample REPL session) in `README.md` immediately so tooling and docs stay in lockstep.
- When you add persistence or indexes, note any file formats, caching assumptions, or performance trade-offs in the relevant module docstrings/comments—agents rely on these to avoid regressions.

## Open gaps & next steps
- There is no schema persistence, query planner, or filtering logic yet; any implementation direction should be confirmed with the user before landing large changes.
- Automated tests are absent; if you introduce `pytest` suites, record invocation commands (`pytest`, `pytest tests/parser_test.py`, etc.) in the README and reference fixtures or sample data.
