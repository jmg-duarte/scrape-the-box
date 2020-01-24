import click
import sys

from stb.commands import callbacks


DEFAULT_DB_NAME = ".stb.db"


@click.group()
def cli():
    pass


@cli.group("fetch")
def fetch():
    """Fetch a page."""


@fetch.command("front")
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]), default="text"
)
@click.option("-o", "--output", type=str, default=sys.stdout)
@click.option(
    "-a",
    "--all",
    "scrape_all",
    flag_value=True,
    is_flag=True,
    callback=callbacks.print_all_warning,
)
@click.option("--db", type=str, flag_value=DEFAULT_DB_NAME)
def fetch_frontpage(output, scrape_all, fmt, db):
    """Fetch the frontpage."""
    from stb.commands.fetch import frontpage

    frontpage.scrape(output, scrape_all, fmt, db)


@fetch.command("thread")
@click.argument("tid", type=str)
@click.option(
    "-f", "--fmt", "--format", type=click.Choice(["text", "json"]), default="text"
)
@click.option("-o", "--output", type=str, default=sys.stdout)
@click.option("--db", type=str, flag_value=DEFAULT_DB_NAME)
def fetch_thread(tid, output, fmt, db):
    """Fetch a discussion page."""
    from stb.commands.fetch import discussion

    discussion.scrape(tid, output, fmt, db)


@cli.group("search")
def search():
    """Search downloaded pages."""


@search.command("thread")
@click.argument("tid", type=str)
@click.argument("search_term", type=str)
@click.option("--db", type=str, default=DEFAULT_DB_NAME)
def search_thread(tid, search_term, db):
    """Search the discussion/thread for comments."""
    from stb.commands.search import discussion

    discussion.search(tid, search_term, db)


@search.command("frontpage")
@click.argument("search_term", type=str)
@click.option("--db", type=str, default=DEFAULT_DB_NAME)
def search_frontpage(search_term, db):
    """Search the frontpage for discussions/threads."""
    from stb.commands.search import frontpage

    frontpage.search(search_term, db)
