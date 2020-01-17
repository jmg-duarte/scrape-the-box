import click
from stb.commands.fetch import scrape_thread_comments


@click.group()
def cli():
    pass


@cli.command('search')
def search():
    print("search")


@cli.group('fetch')
def fetch():
    """Fetches pages"""


@fetch.command('front')
def fetch_frontpage():
    pass


@fetch.command('thread')
@click.argument('tid', type=str)
def fetch_thread(tid):
    scrape_thread_comments(tid)
