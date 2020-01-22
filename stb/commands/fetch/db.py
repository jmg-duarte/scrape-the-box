import sqlite3

CREATE_TABLE_DISCUSSIONS = """
    CREATE TABLE IF NOT EXISTS "discussions" (
        "id"	INTEGER NOT NULL UNIQUE,
        "author"	TEXT NOT NULL,
        "permalink"	TEXT NOT NULL,
        "title"	TEXT NOT NULL,
        PRIMARY KEY("id")
    )
"""
CREATE_TABLE_COMMENTS = """
    CREATE TABLE IF NOT EXISTS "comments" (
        "author"	TEXT NOT NULL,
        "message"	TEXT NOT NULL,
        "discussion_id"	INTEGER NOT NULL,
        "permalink"	TEXT NOT NULL UNIQUE,
        "datetime"	TEXT NOT NULL,
        PRIMARY KEY("permalink")
    )
"""

INSERT_INTO_COMMENTS = """
    INSERT INTO "comments" (
        "discussion_id", 
        "permalink", 
        "author", 
        "message", 
        "datetime"
    ) VALUES (?, ?, ?, ?, ?);
"""
INSERT_INTO_DISCUSSIONS = """
    INSERT INTO "discussions" (
        "id", 
        "permalink", 
        "author", 
        "title"
    ) VALUES (?, ?, ?, ?);
"""


def db_conn_use(db_name, *runnables):
    with sqlite3.connect(db_name) as conn:
        for runnable in runnables:
            runnable(conn)
        conn.commit()
        # conn.close()


def db_cursor_use(db_name, *runnables):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for runnable in runnables:
            runnable(cursor)
        conn.commit()
        # conn.close()


def _get_runnable(f):
    def _f_with_parameters(*args, **kwargs):
        def _using_required(required):
            f(required, *args, **kwargs)

        return _using_required

    return _f_with_parameters


def _dec_w_param(stmt):
    def _get_runnable(f):
        def _f_with_parameters(*args, **kwargs):
            def _using_required(required):
                required.execute(stmt, *args, **kwargs)

            return _using_required

        return _f_with_parameters

    return _get_runnable


@_dec_w_param(CREATE_TABLE_COMMENTS)
def create_comment_table(cursor, stmt):
    pass


@_get_runnable
def db_cursor_create_tables(cursor):
    cursor.execute(CREATE_TABLE_DISCUSSIONS)
    cursor.execute(CREATE_TABLE_COMMENTS)


@_get_runnable
def db_cursor_insert_comment(cursor, comment):
    cursor.execute(INSERT_INTO_COMMENTS, comment)


@_get_runnable
def db_cursor_insert_comments(cursor, comments):
    cursor.executemany(INSERT_INTO_COMMENTS, comments)


@_get_runnable
def db_cursor_insert_discussion(cursor, discussion):
    cursor.execute(INSERT_INTO_COMMENTS, discussion)


@_get_runnable
def db_cursor_insert_discussions(cursor, discussions):
    cursor.executemany(INSERT_INTO_COMMENTS, discussions)
