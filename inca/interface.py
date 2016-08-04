from __future__ import print_function, absolute_import
import click
from . import tk
from . import actions
try:
    input = raw_input
except:
    pass


@click.group()
def handle(*args, **kwargs):
    pass

@click.command()
@click.argument('stack', nargs=1)
@click.argument('name', nargs=1)
def add(stack, name):
    description = input("describe it. (default=none)>  ")
    date = input("what's the timeline (default=inf)>  ")
    urgency = input("how urgent is it  (default=5)>  ")

    if len(description) == 0:
        description = "none"
    if len(date) == 0:
        date = float('inf')
    if len(urgency) == 0:
        urgency = 5

    actions.push(stack, name, description, date, urgency)

@click.command()
@click.argument('stack', nargs=1)
def list(stack):
    actions.list_stack(stack)

@click.command()
@click.argument('stack', nargs=1)
def delete(stack):
    actions.delete_stackitems(stack)

@click.command()
@click.argument('stack', nargs=1)
def stack_iter(stack):
    out = actions.next_item(stack)
    click.echo(out)

@click.command()
@click.argument('filename', nargs=1)
def md2html(filename):
    import subprocess, os, time
    FNULL = open(os.devnull, 'w')
    out = ''.join(filename.split(".")[:-1]+['.html'])
    subprocess.Popen(['pandoc', filename, '-f', 'markdown', '-t', 'html', '-s', '-o', out])
    time.sleep(0.2)
    subprocess.Popen(['gnome-open', out], stdout=FNULL)

@click.command()
@click.argument('denomination', default='eth')
def crypto(denomination):
    x = tk.cbe.get_price(denomination)
    #print(x)
    click.echo(x)
    #return x


handle.add_command(add)
handle.add_command(list)
handle.add_command(delete)
handle.add_command(stack_iter)
handle.add_command(md2html)
handle.add_command(crypto)
'''
@click.command()
@click.argument('name', nargs=1)
@click.argument('item', nargs=-1)
def save(name, item):
    actions.save(item, name)

@click.command()
def dump():
    actions.dump()

@click.command()
@click.argument('name')
def get(name):
    actions.get(name)



handle.add_command(save)
handle.add_command(dump)
handle.add_command(get)'''