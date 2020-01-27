# ⚙ stb

## Installation

Clone this repository

```
git clone https://github.com/jmg-duarte/scrape-the-box.git stb
```

And install with:

```
pip install -r requirements.txt
pip install .
stb
```

### Notes

To use the `--db` flag you need the SQLite FTS5 library available.
A script is provided to download, install and build it for you, just run:

```
sh build_fts5.sh
```

## Getting started

`stb` is supposed to be simple to understand and the flags easy to memorize. 
For each command you can add `--help` to get more information.

```
λ stb --help
Usage: stb [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  fetch   Fetch a page.
  search  Search downloaded pages.
```