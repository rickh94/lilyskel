import click
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.shortcuts import radiolist_dialog

from lilyskel.interface import sub_repl
from lilyskel.interface.common import (ask_to_save, create_instrument,
                                       reorder_instruments,
                                       save_non_interactive)


@click.group(invoke_without_command=True)
@click.pass_context
def instruments(ctx):
    """Change header values """
    _instrument_repl(ctx)


@instruments.command(name="print")
@click.pass_obj
def print_(obj):
    """Print the current instruments"""
    for instrument in obj.piece.instruments:
        print_formatted_text(HTML(f"<b>{instrument.part_name()}</b>"))


@instruments.command()
@click.pass_context
def create(ctx):
    """Create a new instrument"""
    if not ctx.obj.piece.instruments:
        ctx.obj.piece.instruments = []
    ctx.obj.piece.instruments.append(create_instrument(ctx.obj))
    save_non_interactive(ctx)


@instruments.command()
@click.pass_context
def delete(ctx):
    piece = ctx.obj.piece
    delete_index = radiolist_dialog(
        title="Delete Instrument",
        values=[
            (index, instrument.part_name)
            for index, instrument in enumerate(piece.instruments)
        ],
    )
    if delete_index is not None:
        piece.instruments.pop(int(delete_index))
        save_non_interactive(ctx)
    else:
        print_formatted_text(HTML("<b>Aborted!</b>"))


@instruments.command()
@click.pass_context
def reorder(ctx):
    piece = ctx.obj.piece
    piece.instruments = reorder_instruments(piece.instruments)
    save_non_interactive(ctx)


_instrument_repl = sub_repl.create(
    instruments,
    {"message": "lilyskel:edit:instruments> "},
    before_done_callback=ask_to_save,
)
