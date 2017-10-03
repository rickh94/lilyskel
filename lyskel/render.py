"""Render the templates from instrument and piece objects."""
import re
import os
from pathlib import Path
from jinja2 import Environment, PackageLoader


ENV = Environment(loader=PackageLoader('lyskel', 'templates'))
FLAGS = {
    'key_in_partname': False,
    'compress_full_bar_rests': False,
}


def make_instrument(instrument, lyglobal, piece, flags=FLAGS,
                    location=Path('.')):
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
    """
    instemplate = ENV.get_template('ins_part.ly')

    name_prefix = make_name_prefix(piece)
    partfilename = instrument.part_file_name(prefix=name_prefix)

    if not os.path.exists(location):
        os.makedirs(location)
    old_dir = os.getcwd()
    os.chdir(location)

    dirpath = Path(instrument.dir_name())
    partpath = Path(partfilename)
    os.makedirs(dirpath)

    # notes files that need to be included
    include_paths = []
    for movement in piece.movements:
        mov_path = _render_notes(dirpath, piece, instrument, movement)
        include_paths.append(mov_path)

    # part rendering lilypond file
    partrender = instemplate.render(piece=piece, instrument=instrument,
                                    lyglobal=lyglobal, flags=flags,
                                    filename=partfilename)

    with open(partpath, 'w') as partfile:
        partfile.write(partrender)

    include_paths.append(partpath)
    # return the paths for including in the includes.ily
    os.chdir(old_dir)
    return include_paths


def _render_notes(dirpath, piece, instrument, movement):
    notestemplate = ENV.get_template('notes.ily')
    render = notestemplate.render(piece=piece, instrument=instrument,
                                  movement=movement)
    filepath = Path(dirpath, instrument.mov_file_name(movement.num))
    with open(filepath, 'w') as outfile:
        outfile.write(render)

    return filepath


def render_includes(includepaths, piece, extra_includes=[],
                    location=Path('.')):
    """
    Renders the includes file for the piece.

    Arguments:
        includepaths: The auto defined includes from generation of notes files
        a list of Path objects, relative to the prefix path
        extra_includes: more includes defined by the user. a list of Path
        objects
        piece: a Piece object
    """
    old_dir = os.getcwd()
    os.chdir(location)
    template = ENV.get_template('includes.ily')
    render = template.render(piece=piece, extra_includes=extra_includes,
                             includepaths=includepaths)
    includepath = Path('includes.ily')

    with open(includepath, 'w') as includefile:
        includefile.write(render)
    os.chdir(old_dir)


def render_defs(piece, location=Path('.')):
    """Renders the defs file."""
    template = ENV.get_template('defs.ily')
    defspath = Path(location, 'defs.ily')
    render = template.render(piece=piece)

    with open(defspath, 'w') as defsfile:
        defsfile.write(render)


def make_name_prefix(piece):
    """Make the correct filename prefix from the opus or title."""
    if piece.opus:
        name_prefix = re.sub(r'[\,\.po ]', '', piece.opus)
    else:
        name_prefix_tmp = re.sub(r'[\,\.]', '', piece.headers.title).lower()
        name_prefix = re.sub(r'\s', '_', name_prefix_tmp)
    return name_prefix


def render_score(piece, instruments, lyglobal, path_prefix=Path('.')):
    """Renders the score."""
    template = ENV.get_template('score.ly')
    name_prefix = make_name_prefix(piece)
    filename = name_prefix + 'score.ly'
    render = template.render(piece=piece, filename=filename, lyglobal=lyglobal,
                             instruments=instruments)
    score_path = Path(path_prefix, filename)

    with open(score_path, 'w') as scorefile:
        scorefile.write(render)
