from memory import simple
import stacks

def save(x, name=None):
    name = name or str(x)[:5]+"..."
    simple.remember(name, x)


def dump():
    simple.dump()

def get(name):
    print('for the name: {}'.format(name))
    print('\t{}'.format(simple.retrieve(name)))


def push(stackname, shortname, description, date, urgency):
    if not hasattr(stacks, stackname):
        print("Sorry, stack {} is not currently set up".format(stackname))
        return
    stack = getattr(stacks, stackname)
    stack.add(shortname, description, urgency, date)


def list_stack(stackname):
    if not hasattr(stacks, stackname):
        print("Sorry, stack {} is not currently set up".format(stackname))
        return
    stack = getattr(stacks, stackname)

    stack.list_contents()

def delete_stackitems(stackname):
    if not hasattr(stacks, stackname):
        print("Sorry, stack {} is not currently set up".format(stackname))
        return
    stack = getattr(stacks, stackname)
    stack.interactive_delete()

def next_item(stackname):
    if not hasattr(stacks, stackname):
        print("Sorry, stack {} is not currently set up".format(stackname))
        return
    stack = getattr(stacks, stackname)
    return stack.next_item()