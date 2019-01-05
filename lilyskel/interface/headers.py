import click
from prompt_toolkit import prompt, HTML, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import confirm, radiolist_dialog

from lilyskel import info, db_interface
from lilyskel.interface import sub_repl
from lilyskel.interface.common import InsensitiveCompleter, generate_completer, save_non_interactive
from lilyskel.interface.create_commands import create_prompt_command, add_prompt_commands_from_list


@click.group(invoke_without_command=True)
@click.pass_context
def header(ctx):
    """Change header values """
    piece = ctx.obj.piece
    _header_repl(ctx)


def get_composers_from_db(db_):
    return db_interface.explore_table(db_.table("composers"),
                                      search=("name", ""))


def _make_composer_completer(db_):
    return InsensitiveCompleter(get_composers_from_db(db_))


@header.command()
@click.pass_context
def composer(ctx):
    piece = ctx.obj.piece
    completer = ctx.obj.completers.get(
        'composer', generate_completer('composer', ctx.obj, _make_composer_completer))
    current_composer = piece.headers.composer or info.Composer(name='', shortname='', mutopianame='')
    new_composer_input = prompt("Enter Composer: ", completer=completer, default=current_composer.name)
    # return early if composer name isn't changed
    if new_composer_input == current_composer.name:
        print_formatted_text(HTML('<b>No Change Detected</b>'))
        save_non_interactive(ctx)
        return

    # try to load from database
    matches = [item for item in get_composers_from_db(ctx.obj.db) if new_composer_input.lower() in item.lower()]
    if matches and confirm(f"Would you like to load {new_composer_input} from the database? "):
        found = radiolist_dialog(values=[(match, match) for match in matches]) if len(matches) > 1 else matches[0]
        try:
            piece.headers.composer = info.Composer.load_from_db(found, ctx.obj.db)
            save_non_interactive(ctx)
            return
        except NameError:
            pass

    # manually create composer
    new_composer = info.Composer(new_composer_input)
    guess_short_name = new_composer.get_short_name()
    new_composer.shortname = prompt("Enter the abbreviated name of the composer: ",
                                    default=guess_short_name)
    try:
        guess_mutopia_name = new_composer.get_mutopia_name(guess=True)
    except AttributeError:
        guess_mutopia_name = ''
    new_composer.mutopianame = prompt("Enter the mutopia formatted name of the composer "
                                      "or [enter] for none: ", default=guess_mutopia_name)
    if confirm("Would you like to add this composer to the database for easy usage next time?"):
        new_composer.add_to_db(ctx.obj.db)

    piece.headers.composer = new_composer
    save_non_interactive(ctx)


def _make_title_completer(db_):
    return WordCompleter(db_interface.explore_table(
        db_.table("titlewords"), search=("word", "")))


# create generic commands for header
add_prompt_commands_from_list(
    list_of_names=['Subtitle', 'Subsubtitle', 'Poet', 'Meter', 'Arranger', 'Tagline', 'Copyright'],
    help_prefix='Change the piece',
    attribute_prefix='headers',
    group=header
)

title = create_prompt_command(
    name=f'Title',
    help_text=f'Change the piece title',
    attribute=f'headers.title',
    get_completer=_make_title_completer
)

header.add_command(title)
_header_repl = sub_repl.create(header, {'message': 'lilyskel:edit:header> '})
