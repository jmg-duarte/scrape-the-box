import sys
import json
import requests

from typing import Iterable


def write_file(iter: Iterable, file=sys.stdout, fmt="text"):
    if isinstance(file, str):
        with open(file, "w") as f:
            _write(iter, f, fmt)
    else:
        _write(iter, file, fmt)


def _write(iter: Iterable, file, fmt: str):
    if fmt == "text":
        iter = map(str, iter)
        for discussion in iter:
            file.write(discussion)
    elif fmt == "json":
        # TODO there has to be a better way to do this
        json.dump(iter, file, default=lambda x: x.__dict__)
    else:
        raise RuntimeError(f"unknown format: {fmt}")


def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 404:
        # TODO handle this better
        return None
    return response.content