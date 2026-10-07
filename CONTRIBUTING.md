# Contributing

Thanks for helping! Most contributions are **data**, not code: a missing
standard, a wrong letter, a name variant people actually use.

## Repository layout

`data/` holds the JSON data shared by both packages, `py/` the Python
package, `js/` the TypeScript package, `scripts/` shared tools.

## Development setup

```bash
git clone https://github.com/artemmarus/translit-names
cd translit-names
python -m venv .venv && source .venv/bin/activate
pip install -e ./py pytest ruff mypy
pytest --doctest-modules py/src py/tests
ruff check py/src py/tests scripts && (cd py && mypy)
cd js && npm install && npm test
```

## Adding or fixing a scheme

1. Read [`docs/data-format.md`](docs/data-format.md).
2. Create or edit `data/schemes/<id>.json`.
3. Cite the **primary source** (law, official order, standard, LoC/BGN table)
   in `sources`, and record any disagreement between sources in `notes`.
4. Add `samples` — official examples from the source document are best.
   Every sample is a unit test.
5. Run `pytest py/tests/test_schemes.py -k <id>` and
   `python scripts/gen_schemes_doc.py` to refresh `docs/SCHEMES.md`.

## Adding names to the lexicon

Edit the files in `data/names/`. Only add spellings that
people really use (passports, press, registries); `pytest py/tests/test_lexicon_data.py`
checks the structure.

## Reporting a wrong transliteration

Open an issue with: the input, the scheme id, the output you got, the output
you expected, and a link to the rule in the official source.

## TypeScript port

`js/` is a port of the Python package that uses the same `data/`. After changing
Python code or data, regenerate the reference results and run the TS tests:

```bash
python scripts/gen_parity_fixtures.py
cd js && npm install && npm test
```

CI fails if the committed `js/test/fixtures/parity.json` is out of date or if
the TypeScript results differ from Python.

## Code style

`ruff check`, `ruff format`, `mypy` (strict). No runtime dependencies: the
package must stay pure Python with zero required dependencies.
