from pathlib import Path

import click
from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.shortcuts import confirm

from lilyskel import db_interface, info, yaml_interface
from lilyskel.info import Piece
from lilyskel.interface import sub_repl
from lilyskel.interface.common import PATHSAVE, ask_to_save
# from lilyskel.interface.custom_validators_completers import LanguageValidator
from lilyskel.interface.create_commands import create_prompt_command
from lilyskel.interface.header_commands import headers
from lilyskel.interface.instrument_commands import instruments
from lilyskel.interface.movement_commands import movements
from lilyskel.interface.mutopia_commands import mutopia_


@click.group(invoke_without_command=True)
@click.option(
    "-f", "--file-path", required=False, help="Path to yaml config file for project."
)
@click.option("-d", "--db-path", required=False, default=None, help="Path to tinydb.")
@click.pass_context
def edit(ctx, file_path, db_path):
    """Create and edit piece information"""
    if not ctx.obj.config_file_path:
        ctx.obj.config_file_path = get_file_path(file_path)
    if not ctx.obj.piece:
        ctx.obj.piece = get_piece(ctx.obj.config_file_path)
        if ctx.obj.piece.headers.mutopiaheaders:
            ctx.obj.mutopiaheaders = ctx.obj.piece.headers.mutopiaheaders
    if not ctx.obj.db:
        db_ = db_interface.init_db(db_path)
        tables = db_interface.explore_db(db_)
        bootstrap_message = (
            "Lilyskel supports a small database to help with "
            "commonly used items (such as instruments and "
            "composers). You do not appear to have one. "
            "Would you like to copy the included one? "
        )
        if ("composers" not in tables or "instruments" not in tables) and confirm(
            bootstrap_message
        ):
            db_interface.bootstrap_db(db_path)
        ctx.obj.db = db_
    if not ctx.obj.pathsave:
        ctx.obj.pathsave = PATHSAVE
    _edit_repl(ctx)


def get_file_path(file_path):
    if file_path:
        return Path(file_path)
    try:
        with open(PATHSAVE, "r") as savepath:
            return Path(savepath.read())
    except FileNotFoundError:
        return prompt(
            "No path specified or saved. Please enter the path " "to the config file. ",
            completer=PathCompleter(),
        )


def get_piece(file_path):
    try:
        return yaml_interface.read_config(Path(file_path))
    except (ValueError, FileNotFoundError, AttributeError):
        return Piece()


@edit.command(name="print")
@click.pass_obj
def print_(obj):
    """Print the current Piece"""
    print_formatted_text(obj.piece.html())


def _make_language_completer(_):
    return WordCompleter(info.get_valid_languages())


# add commands and repls from metacode
language = create_prompt_command(
    name=f"language",
    help_text=f"Change the note input language",
    attribute=f"piece.language",
    get_completer=_make_language_completer,
)
_edit_repl = sub_repl.create(
    edit, {"message": "lilyskel:edit> "}, before_done_callback=ask_to_save
)
edit.add_command(headers)
edit.add_command(language)
edit.add_command(instruments)
edit.add_command(movements)
edit.add_command(mutopia_)
