import shutil
from pathlib import Path
import click
import tempfile
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import PathCompleter
import os

from lilyskel import yaml_interface, db_interface, info, lynames, render
from lilyskel.interface.common import YNValidator, answered_yes
from lilyskel.interface.edit_prompts import edit_prompt
from .update_db_manually import db

TEMP = tempfile.gettempdir()
PATHSAVE = Path(TEMP, "lilyskel_path")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", required=True,
                # help=( "name of the configuration file for this project.")
)
@click.option("--path", "-p", default=".", help=(
        "path to new directory, defaults to current working directory."))
def init(filename, path):
    """Create the configuration file and set the directory"""
    if ".yaml" not in filename:
        filename = filename + ".yaml"
    filepath = Path(path, filename)
    if filepath.exists():
        overwrite = prompt("File exists. Overwrite? ", validator=YNValidator(),
                           default='N')
        if overwrite.lower()[0] == 'n':
            raise SystemExit(1)
        shutil.copy2(filepath, Path(str(filepath) + ".bak"))
    filepath.open("w").close()
    with open(PATHSAVE, "w") as savepath:
        savepath.write(str(filepath.absolute()))


@cli.command()
@click.option("-f", "--file-path", required=False,
                help="Path to yaml config file for project.")
@click.option("-d", "--db-path", required=False, default=None,
              help="Path to tinydb.")
def edit(file_path, db_path):
    """Create and edit piece information"""
    if not file_path:
        try:
            with open(PATHSAVE, "r") as savepath:
                file_path = Path(savepath.read())
        except FileNotFoundError:
            file_path = prompt("No path specified or saved. Please enter the path "
                   "to the config file. ", completer=PathCompleter())
    try:
        piece = yaml_interface.read_config(Path(file_path))
        print('loaded piece')
        print(piece)
    except (ValueError, FileNotFoundError, AttributeError):
        piece = None
    db = db_interface.init_db(db_path)
    tables = db_interface.explore_db(db)
    if "composers" not in tables or "instruments" not in tables:
        bootstrap = prompt("Lilyskel supports a small database to help with "
                           "commonly used items (such as instruments and "
                           "composers). You do not appear to have one. "
                           "Would you like to copy the included one? ",
                           default='Y', validator=YNValidator())
        if bootstrap.lower()[0] == 'y':
            db_interface.bootstrap_db(db_path)
    edit_prompt(piece, Path(file_path), db, PATHSAVE)


@cli.command()
@click.option("-f", "--file-path", required=False, help="config file to use")
@click.option("-t", "--target-dir", required=False, help="directory to put file skeleton into", default='.')
@click.option("--extra-includes", help="Extra lilypond files to include, comma separated", required=False,
              default=[])
@click.option("--key-in-partname", is_flag=True, default=False, help="Include keys in names of parts.")
@click.option("--compress-full-bar-rests", is_flag=True, default=False,
              help="Set compress_full_bar_rests in part files.")
def build(file_path, target_dir, extra_includes, key_in_partname, compress_full_bar_rests):
    target_dir = Path(target_dir)
    if not file_path:
        possible_configs = [possible for possible in os.listdir(target_dir)
                            if '.yaml' in possible or '.yml' in possible]
        if len(possible_configs) == 0:
            print("No config file found. Please specify one with -f")
            raise SystemExit(1)
        elif len(possible_configs) == 1:
            print(f"Config file found: {possible_configs[0]}")
            use = prompt("Use this config? ", default='Y', validator=YNValidator())
            if answered_yes(use):
                file_path = possible_configs[0]
            else:
                print("Please specify a config file with -f or change to the directory it is in.")
                raise SystemExit(1)
    piece = yaml_interface.read_config(Path(file_path))
    # piece = info.Piece.load(config_data)
    lyglobal = lynames.LyName('global')
    include_paths = []
    flags = {"key_in_partname": key_in_partname, "compress_full_bar_rests": compress_full_bar_rests}
    for instrument in piece.instruments:
        new_includes = render.make_instrument(instrument=instrument, lyglobal=lyglobal,
                                              piece=piece, location=target_dir, flags=flags)
        include_paths.extend(new_includes)
    render.render_includes(include_paths, piece, extra_includes=extra_includes, location=target_dir)
    render.render_defs(piece, location=target_dir)
    render.render_score(piece, piece.instruments, lyglobal, path_prefix=Path('.'))


# adding commands from other files
cli.add_command(db)
