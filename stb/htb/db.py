import sqlite3

from typing import Iterable

from stb.htb.discussion import Discussion
from stb.htb.comment import Comment

CREATE_TABLE_DISCUSSIONS = """
    CREATE TABLE IF NOT EXISTS "discussions" (
        "id"	INTEGER NOT NULL UNIQUE,
        "author"	TEXT NOT NULL,
        "permalink"	TEXT NOT NULL,
        "title"	TEXT NOT NULL,
        PRIMARY KEY("id") ON CONFLICT IGNORE
    )
"""

CREATE_TABLE_COMMENTS = """
    CREATE TABLE IF NOT EXISTS "comments" (
        "discussion_id"	INTEGER NOT NULL,
        "author"	TEXT NOT NULL,
        "message"	TEXT NOT NULL,
        "permalink"	TEXT NOT NULL UNIQUE,
        "datetime"	TEXT NOT NULL,
        PRIMARY KEY("permalink") ON CONFLICT IGNORE
    )
"""

CREATE_VIRTUAL_TABLE_DISCUSSIONS = """
    CREATE VIRTUAL TABLE IF NOT EXISTS "v_discussions" 
        USING fts5(author, title);
"""

CREATE_VIRTUAL_TABLE_COMMENTS = """
    CREATE VIRTUAL TABLE IF NOT EXISTS "v_comments_{}" 
        USING fts5(author, message);
"""

INSERT_INTO_DISCUSSIONS = """
    INSERT INTO "discussions" (
        "id", 
        "author", 
        "permalink", 
        "title"
    ) VALUES (?, ?, ?, ?);
"""

INSERT_INTO_COMMENTS = """
    INSERT INTO "comments" (
        "discussion_id", 
        "permalink", 
        "datetime",
        "author", 
        "message"
    ) VALUES (?, ?, ?, ?, ?);
"""

INSERT_INTO_VIRTUAL_DISCUSSIONS = """
    INSERT INTO "v_discussions" (
        "author", 
        "title"
    ) VALUES (?, ?);
"""


INSERT_INTO_VIRTUAL_COMMENTS = """
    INSERT INTO "v_comments_{}" (
        "author", 
        "message"
    ) VALUES (?, ?);
"""


def _get_runnable(f):
    def _f_with_parameters(*args, **kwargs):
        def _using_required(required):
            f(required, *args, **kwargs)

        return _using_required

    return _f_with_parameters


def conn_use(db_name, *runnables):
    with sqlite3.connect(db_name) as conn:
        for runnable in runnables:
            runnable(conn)
        conn.commit()
        # conn.close()


@_get_runnable
def load_fts(conn):
    conn.enable_load_extension(True)
    conn.load_extension("./fts5")
    conn.enable_load_extension(False)


@_get_runnable
def cursor_exec(conn, *runnables):
    cursor = conn.cursor()
    # TODO maybe return a list of runnable results?
    # TODO maybe create another method
    for r in runnables:
        r(cursor)


@_get_runnable
def cursor_create_discussions_table(cursor):
    cursor.execute(CREATE_TABLE_DISCUSSIONS)


@_get_runnable
def cursor_create_discussion_virtual_table(cursor):
    cursor.execute(CREATE_VIRTUAL_TABLE_DISCUSSIONS)


@_get_runnable
def cursor_create_comments_table(cursor):
    cursor.execute(CREATE_TABLE_COMMENTS)


@_get_runnable
def cursor_create_comments_virtual_table(cursor, discussion_id):
    cursor.execute(CREATE_VIRTUAL_TABLE_COMMENTS.format(discussion_id))


@_get_runnable
def cursor_insert_comments(cursor, comments: Iterable[Comment]):
    comments = map(lambda c: c.as_tuple(), comments)
    cursor.executemany(INSERT_INTO_COMMENTS, comments)


@_get_runnable
def cursor_insert_discussions(cursor, discussions: Iterable[Discussion]):
    discussions = map(lambda d: d.as_tuple(), discussions)
    cursor.executemany(INSERT_INTO_DISCUSSIONS, discussions)


@_get_runnable
def cursor_insert_virtual_discussions(cursor, discussions: Iterable[Discussion]):
    discussions = map(lambda d: (d.author, d.title), discussions)
    cursor.executemany(INSERT_INTO_VIRTUAL_DISCUSSIONS, discussions)


@_get_runnable
def cursor_insert_virtual_comments(cursor, discussion_id, comments: Iterable[Comment]):
    comments = map(lambda d: (d.author, d.message), comments)
    cursor.executemany(INSERT_INTO_VIRTUAL_COMMENTS.format(discussion_id), comments)


@_get_runnable
def cursor_fts_discussions(cursor, search_term):
    # the DISTINCT is a solution to a bigger problem
    # TODO fix the fact that every time a query is made, duplicates are written to the virtual table
    print(search_term)
    cursor.execute(
        """
        SELECT DISTINCT * FROM "v_discussions" WHERE title MATCH ? ORDER BY rank
        """,
        (search_term,),
    )
    print(cursor.fetchall())
