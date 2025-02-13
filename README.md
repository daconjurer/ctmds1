CTMDS
======

A simple Typer-based CLI for price stuff.

The package uses [Poetry 2](https://python-poetry.org/). To install it, run:

```
poetry install
```

## Commands

Check what commands are available with:

```
poetry run python3 -m cli --help
```

To generate random decimals that represent prices:

```
poetry run python3 -m cli random-prices <num-of-elements>
```

where `num-of-elements` is the number of elements to generate (e.g. 100000).

To generate a list of date-price pairs for a given day and a given country:

```
poetry run python3 -m cli daily-prices \
    <date> \
    <country-code> \
    <commodity> \
    --granularity <granularity> \
```

Where date is in the **YYYY-MM-DD** format and the available country codes are:
**GB**, **FR**, **NL**, **DE**.

Where `commodity` can be one of the following: `power`, `natgas` or `crude`.

The `--granularity` flag is optional and `granularity` be either h (hourly) or hh (half-hourly).

## Dev tools

You can run the linting, formatting, tests and static analysis with `make`:

```
make lint
make format
make pyright
make test
make coverage
```

> Note: you can run all checks with `make check`
