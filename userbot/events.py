import sys
import os

from . import app, LOGS

from telethon import events

# Main Handler
def newMessage(**kargs):

    # Telethon args for handler
    pattern = kargs.get('pattern', None)
    kargs.setdefault('forwards', False)
    kargs.setdefault('outgoing', True)

    # Extra args, not based for telethon
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

    # Adding prefix to pattern, for easily use regex
    if pattern is not None and not pattern.startswith('(?i)'):
        kargs['pattern'] = f'(?i){alias}' + pattern

    # Removing extra args for pass to telethon
    kargs.pop('edited')
    kargs.pop('prefix')

    def decorator(func):

        # Handling all exceptions...
        async def exception_handler(arg):
            try:
                await func(arg)
            except Exception as exception:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                LOGS.error(f"Raised {exc_type.__name__}, File: {file_name}, Line: {exc_tb.tb_lineno}")

        # Adding MessageEdit handler
        if edited:
            app.add_event_handler(exception_handler, events.MessageEdited(**kargs))

        # Adding NewMessage handler
        app.add_event_handler(exception_handler, events.NewMessage(**kargs))

        return exception_handler

    return decorator
