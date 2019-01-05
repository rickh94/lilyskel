import functools
from types import FunctionType
from typing import Any

import click
from prompt_toolkit import prompt, HTML

from lilyskel.interface.common import save_non_interactive, generate_completer, AppState


def rgetattr(obj: Any, attr: str, *args):
    def _getattr(obj: Any, attr: str):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def rsetattr(obj: Any, attr: str, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def add_prompt_commands_from_list(list_of_names: list, help_prefix: str, attribute_prefix: str, group: click.Group,
                                  parent_object_name: str = 'piece'):
    for attribute_name in list_of_names:
        attribute_list = [parent_object_name, attribute_prefix, attribute_name.lower()]
        new_command = create_prompt_command(
            name=attribute_name,
            help_text=f'{help_prefix} {attribute_name.lower()}',
            attribute='.'.join(part for part in attribute_list if part),
        )
        group.add_command(new_command)


def create_prompt_command(name: str, attribute: str, help_text: str, *, get_completer: FunctionType = None):
    def _item_prompt():
        ctx = click.get_current_context()
        completer = None
        if get_completer:
            # get the completer from context or generate it
            completer = ctx.obj.completers.get(name, generate_completer(name, ctx.obj, get_completer))
        old_value = rgetattr(ctx.obj, attribute) or ''
        new_value = prompt(HTML(f'<b>Enter {name}:</b> '), default=old_value, completer=completer)
        rsetattr(ctx.obj, attribute, new_value)
        save_non_interactive(ctx)
    return click.Command(name.lower(), callback=_item_prompt, help=help_text)


