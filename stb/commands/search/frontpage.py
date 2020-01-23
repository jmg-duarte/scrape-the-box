from stb.htb import db


def search(search_term, db_name):
    db.conn_use(db_name, db.cursor_exec(db.cursor_fts_discussions(search_term)))

