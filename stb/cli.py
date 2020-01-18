import click

from stb.commands.fetch import frontpage
from stb.commands.fetch import discussion


@click.group()
def cli():
    pass


@cli.command("search")
def search():
    print("search")


@cli.group("fetch")
def fetch():
    """Fetches pages"""


def print_all_warning(ctx, param, all):
    if all:
        r = click.confirm(
            "This will scrape all discussions from the forum. Are you sure you want to continue?",
            default=False,
            show_default=True,
        )
        if not r:
            ctx.abort()
        return r


@fetch.command("front")
@click.option("-o", "--output", type=str, flag_value=None)
@click.option(
    "-a",
    "--all",
    "scrape_all",
    flag_value=True,
    is_flag=True,
    callback=print_all_warning,
)
def fetch_frontpage(output, scrape_all):
    frontpage.scrape(output, scrape_all)


@fetch.command("thread")
@click.argument("tid", type=str)
@click.option("-o", "--output", type=str, flag_value=None)
# @click.option('-f', '--format', flag_value="text", default=True)
def fetch_thread(tid, output):
    discussion.scrape(tid, output)
