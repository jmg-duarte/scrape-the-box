import click


def print_all_warning(ctx, param, all):
    if all:
        r = click.confirm(
            (
                "This will scrape all discussions from the forum.\n"
                "Are you sure you want to continue?"
            ),
            default=False,
            show_default=True,
        )
        if not r:
            ctx.abort()
        return r
