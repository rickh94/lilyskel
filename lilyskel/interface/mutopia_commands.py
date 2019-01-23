import click
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from lilyskel.info import MutopiaHeaders
from lilyskel.interface import create_commands, sub_repl
from lilyskel.interface.common import (ask_to_save, generate_completer,
                                       save_non_interactive)
from lilyskel.interface.custom_validators_completers import (LicenseValidator,
                                                             StyleValidator)
from lilyskel.mutopia import get_licenses, get_styles


@click.group(invoke_without_command=True, name="mutopia")
@click.pass_context
def mutopia_(ctx):
    """Edit headers for submission to the Mutopia Project"""
    if not ctx.obj.mutopiaheaders:
        style_completer = ctx.obj.completers.get(
            "style", generate_completer("style", ctx.obj, _get_style_completer)
        )
        license_completer = ctx.obj.completers.get(
            "license", generate_completer("license", ctx.obj, _get_license_completer)
        )
        source = source_prompt()
        style = style_prompt(style_completer)
        license_ = license_prompt(license_completer)
        ctx.obj.mutopiaheaders = MutopiaHeaders(
            source=source, style=style, license=license_
        )
    _mutopia_repl(ctx)


@mutopia_.command("print")
@click.pass_obj
def print_(obj):
    print(obj.mutopiaheaders.dump())


@mutopia_.command("license")
@click.pass_context
def license_(ctx):
    license_completer = ctx.obj.completers.get(
        "license", generate_completer("license", ctx.obj, _get_license_completer)
    )
    ctx.obj.mutopiaheaders.license = license_prompt(
        license_completer, ctx.obj.mutopiaheaders.license
    )
    save_non_interactive(ctx)


@mutopia_.command()
@click.pass_context
def style(ctx):
    style_completer = ctx.obj.completers.get(
        "style", generate_completer("style", ctx.obj, _get_style_completer)
    )
    ctx.obj.mutopiaheaders.style = style_prompt(
        style_completer, ctx.obj.mutopiaheaders.style
    )
    save_non_interactive(ctx)


@mutopia_.command()
@click.pass_context
def source(ctx):
    ctx.obj.mutopiaheaders.source = source_prompt(ctx.obj.mutopiaheaders.source)
    save_non_interactive(ctx)


def source_prompt(default=""):
    return prompt("Enter the source: ", default=default)


def style_prompt(completer, default=""):
    return prompt(
        "Enter the style: ",
        completer=completer,
        validator=StyleValidator(),
        default=default,
    )


def license_prompt(completer, default=""):
    return prompt(
        "Enter the license: ",
        completer=completer,
        validator=LicenseValidator(),
        default=default,
    )


def _get_style_completer(_db):
    return WordCompleter(get_styles())


def _get_license_completer(_db):
    return WordCompleter(get_licenses())


create_commands.add_prompt_commands_from_list(
    group=mutopia_,
    list_of_names=[
        "maintainer",
        "maintainerEmail",
        "maintainerWeb",
        "mutopiatitle",
        "mutopiapoet",
        "mutopiapoet",
        "mutopiaopus",
        "date",
        "moreinfo",
        "done",
    ],
    help_prefix="Change Mutopia Header ",
    attribute_prefix="",
    parent_object_name="mutopiaheaders",
)

_mutopia_repl = sub_repl.create(
    mutopia_, {"message": "lilyskel:edit:mutopia> "}, before_done_callback=ask_to_save
)
