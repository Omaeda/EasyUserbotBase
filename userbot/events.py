from telethon import events
from . import app
def newMessage(**args):

    pattern = args.get('pattern', None)
    prefix = args.get('prefix', [])

    alias = '['

    if len(prefix) > 0:
        for x in prefix:
            if x != ']' and x != '[':
                if x == '/':
                    alias += f'\{x}'
                else:
                    alias += x
        alias += ']'
    else:
        alias = ''

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = f'(?i){alias}' + pattern

    del args['prefix']

    def decorator(func):
        app.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator
