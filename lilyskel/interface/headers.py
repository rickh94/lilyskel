import click
from prompt_toolkit import prompt, HTML
from prompt_toolkit.completion import WordCompleter

from lilyskel import info, db_interface
from lilyskel.interface import sub_repl
from lilyskel.interface.create_commands import create_prompt_command, add_prompt_commands_from_list
from lilyskel.interface.edit_prompts import composer_prompt


@click.group(invoke_without_command=True)
@click.pass_context
def header(ctx):
    """Change header values """
    piece = ctx.obj.piece
    # prompt_help = (
    #     "You may edit any of the following headers:\n"
    #     "title\t\tcomposer\n"
    #     "dedication\tsubtitle\n"
    #     "subsubtitle\tpoet\n"
    #     "meter\t\tarranger\n"
    #     "tagline\t\tcopyright\n"
    #     f"Enter {BOLD}print{END} to print the current headers and {BOLD}done{END} to finish"
    #     "and return to the main prompt."
    # )
    # print(prompt_help)
    # titlewords = WordCompleter(db_interface.explore_table(
    #     db.table("titlewords"), search=("word", "")))
    # field_completer = WordCompleter(["title", "composer", "subtitle", "subsubtitle",
    #                                  "poet", "meter", "arranger", "tagline", "copyright",
    #                                  "print", "done"])
    # if curr_headers is None:
    #     composer = composer_prompt(db)
    #     title = prompt("Enter Title: ", completer=titlewords)
    #     curr_headers = info.Headers(title=title, composer=composer)
    # while 1:
    #     # DEBUG LINE
    #     # print(curr_headers)
    #     command = prompt("Headers> ", completer=field_completer)
    #     if len(command) == 0:
    #         continue
    #     field = command.lower().strip()
    #     if field == "title":
    #         title = prompt(
    #             "Current title is \"{}\" enter a new title or press "
    #             "enter to keep the current one: ".format(
    #                 curr_headers.title
    #             )
    #         )
    #         if len(title) != 0:
    #             curr_headers.title = title
    #     elif "comp" in field:
    #         change_comp = prompt("Current composer is {}. Would you like to change "
    #                              "it? ".format(curr_headers.composer.name), default='N',
    #                              validator=YNValidator())
    #         if answered_yes(change_comp):
    #             curr_headers.composer = composer_prompt(db)
    #     elif field in ["dedication", "subtitle", "subsubtitle", "poet",
    #                    "meter", "arranger", "tagline", "copyright"]:
    #         print("{} is {}".format(field, getattr(curr_headers, field, "blank")))
    #         new = prompt(f"Enter value for {field} or press enter to leave unchanged: ")
    #         if len(new) > 0:
    #             setattr(curr_headers, field, new)
    #     # Logistical commands
    #     elif field[0] == 'h':
    #         print(prompt_help)
    #     elif field[0] == 'p':
    #         print(curr_headers)
    #     elif field[0] == 'd' or field == "save":
    #         print("Saving headers")
    #         return curr_headers
    #     else:
    #         print(INVALID)
    _header_repl(ctx)


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
