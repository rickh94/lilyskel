"""Render the templates from instrument and piece objects."""
from jinja2 import Environment, PackageLoader
import os
from pathlib import Path


ENV = Environment(loader=PackageLoader('lyskel', 'templates'))
FLAGS = {
    'key_in_partname': False,
    'compress_full_bar_rests': False,
}


def make_instrument(instrument, lyglobal, piece, flags=FLAGS, prefix=None,
                    moreincludes=[]):
    """
    Create all the files related to an instrument.

    Arguments:
        instrument: An lynames.Instrument object.
        lyglobal: An lynames.LyName object with the 'global' name.
        piece: An info.Piece object (with movement info).
        flags: a dict of the options for rendering the instrument part:
            key_in_partname: bool, compress_full_bar_rests: bool.
            If not supplied, both will default to false.
        prefix: path prefix for generation of the directory structure. Defaults
            to current working directory. Relative paths are prefered.
        moreincluds: a list of additional files to include. Defaults to empty
            list.
    """
    instemplate = ENV.get_template('ins_part.ly')
    notestemplate = ENV.get_template('notes.ily')
    if not prefix:
        # It is for mobility of the directory tree to use relative paths, so
        # '.' is default so the path will be relative.
        prefix = Path('.')

    partfilename = instrument.part_file_name(prefix=piece.opus)
    dirpath = Path(prefix, instrument.dir_name())
    partpath = Path(prefix, partfilename)
    os.makedirs(dirpath)

    include_paths = []
    for movement in piece.movements:
        mov_path = _render_notes(dirpath, piece, instrument, movement)
        include_paths.append(mov_path)

    partrender = instemplate.render(piece=piece, instrument=instrument,
                                    lyglobal=lyglobals, flags=flags,
                                    moreincludes=moreincludes,
                                    filename=partfilename)

    with open(partpath, 'w') as partfile:
        partfile.write(partrender)

    include_paths.append(partpath)
    return include_paths


def _render_notes(dirpath, piece, instrument, movement):
    # TODO: add to includes file
    render = notestemplate.render(piece=piece, instrument=instrument,
                                  movement=movement)
    tmppath = Path(dirpath, instrument.mov_file_name(movement.num))
    with open(tmppath, 'w') as outfile:
        outfile.write(render)

    return tmppath


def render_includes(includepaths, piece):
    """
    Renders the includes file for the
    """
