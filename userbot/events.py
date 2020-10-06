from . import app, LOGS

from telethon import events

# HANDLER 
def newMessage(**kargs):

    # KARGS FOR HANDLER
    pattern = kargs.get('pattern', None)

    kargs.setdefault('forwards', False)
    kargs.setdefault('outgoing', True)

    # EXTRA ARGS
    prefix = kargs.setdefault('prefix', ['.', '/'])
    edited = kargs.setdefault('edited', True)

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

    # ADD PREFIX TO PATTERN
    if pattern is not None and not pattern.startswith('(?i)'):
        kargs['pattern'] = f'(?i){alias}' + pattern

    # REMOVE EXTRA ARGS
    kargs.pop('edited')
    kargs.pop('prefix')

    def decorator(func):
        if edited:
            app.add_event_handler(func, events.MessageEdited(**kargs))
        app.add_event_handler(func, events.NewMessage(**kargs))
        return func

    return decorator
