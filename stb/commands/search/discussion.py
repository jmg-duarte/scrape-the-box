import json
import sys

from stb.htb import db


def search(thread_id, search_term, db_name):
    db.conn_use(
        db_name,
        db.cursor_exec(
            db.cursor_fts_comments(thread_id, search_term, _search_callback)
        ),
    )


def _search_callback(results):
    json.dump(
        _results_to_json_array(results), indent="    ", fp=sys.stdout,
    )


def _results_to_json_array(results):
    return list(
        map(lambda result: {"author": result[0], "message": result[1]}, results)
    )
