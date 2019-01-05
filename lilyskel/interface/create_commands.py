import functools

import click
from prompt_toolkit import prompt, HTML

from lilyskel.interface.common import save_non_interactive, generate_completer


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def add_prompt_commands_from_list(list_of_names, help_prefix, attribute_prefix, group):
    for attribute_name in list_of_names:
        new_command = create_prompt_command(
            name=attribute_name,
            help_text=f'{help_prefix} {attribute_name.lower()}',
            attribute=f'{attribute_prefix}.{attribute_name.lower()}'
        )
        group.add_command(new_command)


def create_prompt_command(name, attribute, help_text, *, get_completer=None):
    def _item_prompt():
        ctx = click.get_current_context()
        completer = None
        if get_completer:
            # get the completer from context or generate it
            completer = ctx.obj.completers.get(name, generate_completer(name, ctx.obj, get_completer))
        piece = ctx.obj.piece
        old_value = rgetattr(piece, attribute) or ''
        new_value = prompt(HTML(f'<b>Enter {name}:</b> '), default=old_value, completer=completer)
        rsetattr(piece, attribute, new_value)
        save_non_interactive(ctx)
    return click.Command(name.lower(), callback=_item_prompt, help=help_text)


