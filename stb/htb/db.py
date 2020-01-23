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


def _get_runnable(f):
    def _f_with_parameters(*args, **kwargs):
        def _using_required(required):
            f(required, *args, **kwargs)

        return _using_required

    return _f_with_parameters


def db_conn_use(db_name, *runnables):
    with sqlite3.connect(db_name) as conn:
        for runnable in runnables:
            runnable(conn)
        conn.commit()
        # conn.close()


@_get_runnable
def db_cursor_exec(conn, *runnables):
    cursor = conn.cursor()
    for r in runnables:
        r(cursor)


def db_cursor_use(db_name, *runnables):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for runnable in runnables:
            runnable(cursor)
        conn.commit()
        # conn.close()


@_get_runnable
def db_cursor_create_discussions_table(cursor):
    cursor.execute(CREATE_TABLE_DISCUSSIONS)


@_get_runnable
def db_cursor_create_comments_table(cursor):
    cursor.execute(CREATE_TABLE_COMMENTS)


@_get_runnable
def db_cursor_insert_comment(cursor, comment: Comment):
    cursor.execute(INSERT_INTO_COMMENTS, comment.as_tuple())


@_get_runnable
def db_cursor_insert_comments(cursor, comments: Iterable[Comment]):
    comments = map(lambda c: c.as_tuple(), comments)
    cursor.executemany(INSERT_INTO_COMMENTS, comments)


@_get_runnable
def db_cursor_insert_discussion(cursor, discussion: Discussion):
    cursor.execute(INSERT_INTO_DISCUSSIONS, discussion.as_tuple())


@_get_runnable
def db_cursor_insert_discussions(cursor, discussions: Iterable[Discussion]):
    discussions = map(lambda d: d.as_tuple(), discussions)
    cursor.executemany(INSERT_INTO_DISCUSSIONS, discussions)
