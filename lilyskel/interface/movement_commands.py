import bs4
import click
import requests
from prompt_toolkit import HTML, print_formatted_text, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog
from titlecase import titlecase

from lilyskel import info
from lilyskel.interface import sub_repl
from lilyskel.interface.common import (ask_to_save, generate_completer,
                                       save_non_interactive)
from lilyskel.interface.custom_validators_completers import (InsensitiveCompleter,
                                                             ModeValidator,
                                                             NoteValidator)


@click.group(invoke_without_command=True)
@click.pass_context
def movements(ctx):
    """Edit piece movements."""
    piece = ctx.obj.piece
    if not piece.movements:
        piece.movements = []
    _movements_repl(ctx)


@movements.command()
@click.pass_context
def create(ctx):
    """Create a new movement"""
    piece = ctx.obj.piece
    tempo_completer = ctx.obj.completers.get(
        "tempo", generate_completer("tempo", ctx.obj, _get_tempo_completer)
    )
    mode_completer = ctx.obj.completers.get(
        "mode", generate_completer("mode", ctx.obj, _get_mode_completer)
    )
    new_mov_num = len(piece.movements) + 1
    piece.movements.append(
        movement_prompt(tempo_completer, mode_completer, new_mov_num)
    )
    save_non_interactive(ctx)


@movements.command()
@click.pass_context
def update(ctx):
    """Update the info for a movement"""
    piece = ctx.obj.piece
    mov_idx = radiolist_dialog(
        title="Update Movement",
        text="Select a movement to update",
        values=[
            (index, str(movement)) for index, movement in enumerate(piece.movements)
        ],
    )
    if mov_idx is None:
        print_formatted_text("Aborted!")
        return
    movement_to_update = piece.movements.pop(mov_idx)
    tempo_completer = ctx.obj.completers.get(
        "tempo", generate_completer("tempo", ctx.obj, _get_tempo_completer)
    )
    mode_completer = ctx.obj.completers.get(
        "mode", generate_completer("mode", ctx.obj, _get_mode_completer)
    )
    new_mov = movement_prompt(
        tempo_completer,
        mode_completer,
        number=movement_to_update.num,
        existing_tempo=movement_to_update.tempo,
        existing_key=movement_to_update.key,
        existing_time=movement_to_update.time,
    )
    print_formatted_text("Movement Updated")
    piece.movements.insert(mov_idx, new_mov)
    save_non_interactive(ctx)


@movements.command()
@click.pass_context
def delete(ctx):
    piece = ctx.obj.piece
    mov_idx = radiolist_dialog(
        title="Delete Movement",
        text="Select a movement to delete",
        values=[
            (index, str(movement)) for index, movement in enumerate(piece.movements)
        ],
    )
    if mov_idx is None:
        print_formatted_text("Aborted!")
        return
    piece.movements.pop(mov_idx)
    # update numbers of remaining movements
    for i in range(mov_idx, len(piece.movements)):
        piece.movements[i].num = piece.movements[i].num - 1
    print_formatted_text("Movement Deleted")
    save_non_interactive(ctx)


@movements.command("print")
@click.pass_obj
def print_(obj):
    """Print the current movements"""
    print_formatted_text(HTML("<b>Movements:</b>"))
    for movement in obj.piece.movements:
        print_formatted_text(str(movement))


def movement_prompt(
    tempo_completer: InsensitiveCompleter,
    mode_completer: WordCompleter,
    number: int,
    existing_tempo: str = "",
    existing_time: str = "",
    existing_key: info.KeySignature = info.KeySignature("", ""),
):
    new_mov_tempo = prompt(
        "Enter tempo (optional): ", completer=tempo_completer, default=existing_tempo
    )
    new_mov_time = prompt("Enter time signature (optional): ", default=existing_time)
    new_mov_key_note = prompt(
        "Enter key note: ", validator=NoteValidator(), default=existing_key.note
    )
    new_mov_key_mode = prompt(
        "Enter key mode: ",
        completer=mode_completer,
        validator=ModeValidator(),
        default=existing_key.mode,
    )
    new_mov_key = info.KeySignature(note=new_mov_key_note, mode=new_mov_key_mode)
    return info.Movement(
        num=number, tempo=new_mov_tempo, time=new_mov_time, key=new_mov_key
    )


def _get_tempo_words():
    wiki = requests.get("https://en.wikipedia.org/wiki/Tempo")
    wiki_soup = bs4.BeautifulSoup(wiki.text, "html.parser")
    tempos = []
    for title in [
        "Basic_tempo_markings",
        "French_tempo_markings",
        "German_tempo_markings",
    ]:
        title = wiki_soup.find(id=title)
        tempos_soup = title.find_next("ul")
        tempos_temp = []
        for item in tempos_soup.find_all("i"):
            tempos_temp.extend(titlecase(item.text).split(" "))
        tempos.extend(tempos_temp)
    return tempos


def _get_tempo_completer(_db):
    return InsensitiveCompleter(_get_tempo_words())


def _get_mode_completer(_db):
    return WordCompleter(info.get_allowed_modes())


_movements_repl = sub_repl.create(
    movements,
    {"message": "lilyskel:edit:movements> "},
    before_done_callback=ask_to_save,
)
