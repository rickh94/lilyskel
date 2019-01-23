import os
import shutil
from pathlib import Path

import click
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm

from lilyskel import info, lynames, render, yaml_interface
from lilyskel.interface import sub_repl
from lilyskel.interface.common import PATHSAVE, AppState
from lilyskel.interface.custom_validators_completers import YNValidator
from lilyskel.interface.edit_commands import edit

from .db_commands import db


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Create skeleton folders and files for lilypond project."""
    ctx.obj = AppState()
    _lilyskel_repl(ctx)


@cli.command()
@click.argument("filename", required=True)
@click.option(
    "--path",
    "-p",
    default=".",
    help=("path to new directory, defaults to current working directory."),
)
def init(filename, path):
    """Create the configuration file and set the directory"""
    if ".yaml" not in filename and ".yml" not in filename:
        filename = filename + ".yaml"
    filepath = Path(path, filename)
    if filepath.exists():
        overwrite = prompt(
            "File exists. Overwrite? ", validator=YNValidator(), default="N"
        )
        if overwrite.lower()[0] == "n":
            raise SystemExit(1)
        shutil.copy2(filepath, Path(str(filepath) + ".bak"))
    yaml_interface.write_config(filepath, info.Piece())
    with open(PATHSAVE, "w") as save_path:
        save_path.write(str(filepath.absolute()))


@cli.command()
@click.option("-f", "--file-path", required=False, help="config file to use")
@click.option(
    "-t",
    "--target-dir",
    required=False,
    help="directory to put file skeleton into",
    default=".",
)
@click.option(
    "--extra-includes",
    help="Extra lilypond files to include, comma separated",
    required=False,
    default=[],
)
@click.option(
    "--key-in-partname",
    is_flag=True,
    default=False,
    help="Include keys in names of parts.",
)
@click.option(
    "--compress-full-bar-rests",
    is_flag=True,
    default=False,
    help="Set compress_full_bar_rests in part files.",
)
def build(
    file_path, target_dir, extra_includes, key_in_partname, compress_full_bar_rests
):
    """Create files and folders from configuration file."""
    target_dir = Path(target_dir)
    if not file_path:
        possible_configs = [
            possible
            for possible in os.listdir(target_dir)
            if ".yaml" in possible or ".yml" in possible
        ]
        if len(possible_configs) == 0:
            print("No config file found. Please specify one with -f")
            raise SystemExit(1)
        elif len(possible_configs) == 1:
            print(f"Config file found: {possible_configs[0]}")
            if confirm("Use this config?"):
                file_path = possible_configs[0]
            else:
                print(
                    "Please specify a config file with -f or "
                    "change to the directory it is in."
                )
                raise SystemExit(1)
    piece = yaml_interface.read_config(Path(file_path))
    lyglobal = lynames.LyName("global")
    include_paths = []
    flags = {
        "key_in_partname": key_in_partname,
        "compress_full_bar_rests": compress_full_bar_rests,
    }
    global_file = render.make_global(lyglobal, piece, location=target_dir)
    include_paths.extend(global_file)
    for instrument in piece.instruments:
        new_includes = render.make_instrument(
            instrument=instrument,
            lyglobal=lyglobal,
            piece=piece,
            location=target_dir,
            flags=flags,
        )
        include_paths.extend(new_includes)
    render.render_includes(
        include_paths, piece, extra_includes=extra_includes, location=target_dir
    )
    render.render_defs(piece, location=target_dir)
    render.render_score(piece, piece.instruments, lyglobal, path_prefix=Path("."))


# metacode to configure interface
cli.add_command(db)
cli.add_command(edit)
_lilyskel_repl = sub_repl.create(cli, {"message": "lilyskel> "})
