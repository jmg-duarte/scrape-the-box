import click
from stb.commands.fetch.thread import scrape_thread_comments


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
@click.option('-o', '--output', flag_value=None)
# @click.option('-f', '--format', flag_value="text", default=True)
def fetch_thread(tid, output):
    scrape_thread_comments(tid, output)
