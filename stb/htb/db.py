import sqlite3

from typing import Iterable

from stb.htb.discussion import Discussion
from stb.htb.comment import Comment

CREATE_TRIGGER_DISCUSSIONS = """
    CREATE TRIGGER IF NOT EXISTS "trigger_discussions" BEFORE
    INSERT ON "discussions"
    FOR EACH ROW WHEN (
        NOT EXISTS(
            SELECT 1 FROM discussions WHERE discussions.id IS NEW.id
        )
    ) 
    BEGIN
        INSERT INTO "v_discussions" VALUES (NEW.author, NEW.title);
    END
"""

CREATE_TRIGGER_COMMENTS = """
    CREATE TRIGGER IF NOT EXISTS "trigger_comments_{tid}" BEFORE
    INSERT ON "comments"
    FOR EACH ROW WHEN (
        NOT EXISTS(
            SELECT 1 FROM comments WHERE comments.permalink IS NEW.permalink
        )
    ) 
    BEGIN
        INSERT INTO "v_comments_{tid}" VALUES (NEW.author, NEW.message);
    END
"""

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
        PRIMARY KEY("permalink")
    )
"""

CREATE_VIRTUAL_TABLE_DISCUSSIONS = """
    CREATE VIRTUAL TABLE IF NOT EXISTS "v_discussions" 
        USING fts5(author, title);
"""

CREATE_VIRTUAL_TABLE_COMMENTS = """
    CREATE VIRTUAL TABLE IF NOT EXISTS "v_comments_{tid}" 
        USING fts5(author, message);
"""

INSERT_INTO_DISCUSSIONS = """
    INSERT INTO "discussions" (
        "id", 
        "author", 
        "permalink", 
        "title"
    ) VALUES (?, ?, ?, ?)
    ON CONFLICT DO NOTHING;
"""

INSERT_INTO_COMMENTS = """
    INSERT INTO "comments" (
        "discussion_id", 
        "permalink", 
        "datetime",
        "author", 
        "message"
    ) VALUES (?, ?, ?, ?, ?)
    ON CONFLICT DO NOTHING;
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

SELECT_DISCUSSIONS = """
    SELECT * 
    FROM "v_discussions" 
    WHERE title MATCH ? 
    ORDER BY rank
"""

SELECT_COMMENTS = """
    SELECT * 
    FROM "v_comments_{tid}" 
    WHERE title MATCH ? 
    ORDER BY rank
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
    conn.load_extension("/usr/local/lib/stb/fts5")
    conn.enable_load_extension(False)


@_get_runnable
def cursor_exec(conn, *runnables):
    cursor = conn.cursor()
    # TODO maybe return a list of runnable results?
    # TODO maybe create another method
    for r in runnables:
        r(cursor)


@_get_runnable
def cursor_create_discussions(cursor):
    cursor.execute(CREATE_TABLE_DISCUSSIONS)
    cursor.execute(CREATE_VIRTUAL_TABLE_DISCUSSIONS)
    cursor.execute(CREATE_TRIGGER_DISCUSSIONS)


@_get_runnable
def cursor_create_comments(cursor, discussion_id):
    cursor.execute(CREATE_TABLE_COMMENTS)
    cursor.execute(CREATE_VIRTUAL_TABLE_COMMENTS.format(tid=discussion_id))
    cursor.execute(CREATE_TRIGGER_COMMENTS.format(tid=discussion_id))


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
    # cursor.executemany(INSERT_INTO_VIRTUAL_DISCUSSIONS, discussions)


@_get_runnable
def cursor_insert_virtual_comments(cursor, discussion_id, comments: Iterable[Comment]):
    comments = map(lambda d: (d.author, d.message), comments)
    # cursor.executemany(INSERT_INTO_VIRTUAL_COMMENTS.format(discussion_id), comments)


@_get_runnable
def cursor_fts_discussions(cursor, search_term, callback):
    cursor.execute(
        SELECT_DISCUSSIONS, (search_term,),
    )
    callback(cursor.fetchall())


@_get_runnable
def cursor_fts_comments(cursor, thread_id, search_term, callback):
    try:
        cursor.execute(
            SELECT_COMMENTS.format(tid=thread_id), (thread_id, search_term,),
        )
    except sqlite3.OperationalError as e:
        print(
            f"Thread {thread_id} was not found.\nHave you tried downloading it with:\n\n\tstb fetch thread {thread_id} --db"
        )
        return
    callback(cursor.fetchall())
