from memory import simple

def save(x, name=None):
    name = name or str(x)[:5]+"..."
    simple.remember(name, x)


def dump():
    simple.dump()