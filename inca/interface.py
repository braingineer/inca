from __future__ import print_function, absolute_import
import click
from . import actions


@click.group()
def handle(*args, **kwargs):
    pass

@click.command()
@click.argument('name', nargs=1)
@click.argument('item', nargs=-1)
def save(name, item):
    actions.save(item, name)

@click.command()
def dump():
    actions.dump()

handle.add_command(save)
handle.add_command(dump)