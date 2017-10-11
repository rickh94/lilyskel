"""Tests that template files produce the correct output."""
import os
from pathlib import Path
import pytest
from jinja2 import Environment, PackageLoader
from lilyskel import info
from lilyskel import lynames


def test_defs(tmpdir, jinja_env, piece1, piece2):
    """Test rendering the defs template."""
    defstemplate = jinja_env.get_template('defs.ily')
    with open(Path(tmpdir, 'defs_test1.ily'), 'w') as defs1:
        defs1.write(defstemplate.render(piece=piece1))
    with open(Path(tmpdir, 'defs_test2.ily'), 'w') as defs2:
        defs2.write(defstemplate.render(piece=piece2))

    with open(Path(tmpdir, 'defs_test1.ily'), 'r') as defs1:
        test1 = defs1.read()
    with open(Path(tmpdir, 'defs_test2.ily'), 'r') as defs2:
        test2 = defs2.read()

    assert 'Johann Sebastian Bach' in test1,\
        "Composer name should be in the file"
    assert 'mytagline' in test1, "Tagline should be in the file"
    assert 'Test Piece' in test1, "Title should be in the file."

    assert 'Claude Debussy' in test2, "Composer name should be in the file."
    assert 'mytagline' in test2, "Tagline should be in the file."
    assert '1234' in test2, "date should be in the file"
    assert 'Test Piece' in test2, "title should be in the file"
    assert 'A nonexistent piece' in test2, "subtitle should be in the file"
    assert 'To my test functions' in test2, "dedication should be in the file"


def test_ins_part(tmpdir, jinja_env, test_ins, test_ins3, piece1,
                  piece2, piano):
    """Tests rendering an instrument part."""
    instemplate = jinja_env.get_template('ins_part.ly')
    lyglobals = lynames.LyName(name='global')
    flags1 = {
        'key_in_partname': False,
        'compress_full_bar_rests': True,
    }
    flags2 = {
        'key_in_partname': True,
        'compress_full_bar_rests': False
    }
    render1 = instemplate.render(piece=piece1, instrument=test_ins,
                                 lyglobal=lyglobals, flags=flags1,
                                 filename='inspart_test1.ly')
    render2 = instemplate.render(piece=piece2, instrument=test_ins3,
                                 lyglobal=lyglobals, flags=flags2,
                                 filename='inspart_test2.ly')
    render3 = instemplate.render(piece=piece1, instrument=piano,
                                 lyglobal=lyglobals, flags=flags1,
                                 filename='piano_part.ly')
    with open(Path(tmpdir, 'inspart_test1.ly'), 'w') as part:
        part.write(render1)
    with open(Path(tmpdir, 'inspart_test2.ly'), 'w') as part:
        part.write(render2)
    with open(Path(tmpdir, 'piano_part.ly'), 'w') as part:
        part.write(render3)

    with open(Path(tmpdir, 'inspart_test1.ly'), 'r') as part:
        part_test1 = part.read()
    with open(Path(tmpdir, 'inspart_test2.ly'), 'r') as part:
        part_test2 = part.read()
    with open(Path(tmpdir, 'piano_part.ly'), 'r') as part:
        part_test3 = part.read()

    assert '\\version' in part_test1
    assert '\\include "defs.ily"' in part_test1
    assert '\\violin_one_first_mov' in part_test1
    assert '\\global_second_mov' in part_test1
    assert '\\compressFullBarRests' in part_test1

    assert '\\version' in part_test2
    assert '\\include "defs.ily"' in part_test2
    assert '\\clarinet_in_bb_first_mov' in part_test2
    assert '\\clarinet_in_bb_fourth_mov' in part_test2
    assert '\\global_second_mov' in part_test2
    assert '\\compressFullBarRests' not in part_test2
    assert 'Op. 15' in part_test2

    assert '\\version' in part_test3
    assert '\\include "defs.ily"' in part_test3
    assert '\\piano_first_mov_LH' in part_test3
    assert '\\piano_third_mov_RH' in part_test3
    assert 'PianoStaff' in part_test3


@pytest.fixture
def global_ins():
    """An object for global info."""
    return lynames.LyName(name='global')


def test_notes(tmpdir, jinja_env, test_ins, test_ins2, three_movs,
               piece1, global_ins, piano):
    """Test generating the notes template parts."""
    template = jinja_env.get_template('notes.ily')
    for ins in [global_ins, test_ins, test_ins2, piano]:
        dirpath = Path(tmpdir, ins.dir_name())
        os.makedirs(dirpath)
        for mov in piece1.movements:
            render = template.render(piece=piece1, instrument=ins,
                                     movement=mov)
            with open(Path(dirpath, ins.mov_file_name(mov.num)), 'w') as out:
                out.write(render)

    globalpath = Path(tmpdir, 'global')
    test_ins_path = Path(tmpdir, 'violin1')
    test_ins2_path = Path(tmpdir, 'violoncello2')
    piano_path = Path(tmpdir, 'piano')

    with open(Path(globalpath, 'global_1.ily'), 'r') as file1:
        global1 = file1.read()
    with open(Path(globalpath, 'global_2.ily'), 'r') as file2:
        global2 = file2.read()
    with open(Path(globalpath, 'global_3.ily'), 'r') as file3:
        global3 = file3.read()
    with open(Path(test_ins_path, 'violin1_1.ily'), 'r') as file4:
        test_ins_1 = file4.read()
    with open(Path(test_ins_path, 'violin1_2.ily'), 'r') as file5:
        test_ins_2 = file5.read()
    with open(Path(test_ins_path, 'violin1_3.ily'), 'r') as file6:
        test_ins_3 = file6.read()
    with open(Path(test_ins2_path, 'violoncello2_1.ily'), 'r') as file7:
        test_ins2_1 = file7.read()
    with open(Path(test_ins2_path, 'violoncello2_2.ily'), 'r') as file8:
        test_ins2_2 = file8.read()
    with open(Path(test_ins2_path, 'violoncello2_3.ily'), 'r') as file9:
        test_ins2_3 = file9.read()
    with open(Path(piano_path, 'piano_1.ily'), 'r') as file10:
        piano_1 = file10.read()
    with open(Path(piano_path, 'piano_2.ily'), 'r') as file11:
        piano_2 = file11.read()
    with open(Path(piano_path, 'piano_3.ily'), 'r') as file12:
        piano_3 = file12.read()

    assert 'global_first_mov' in global1, "should have variable"
    assert 'Allegro' in global1, "global should have tempo"
    assert 'global_second_mov' in global2, "should have variable"
    assert 'global_third_mov' in global3, "should have variable"
    assert 'violin_one_first_mov' in test_ins_1, "should have variable"
    assert '\\clef "treble"' in test_ins_1, "should have clef"
    assert 'violin_one_second_mov' in test_ins_2, "should have variable"
    assert 'violin_one_third_mov' in test_ins_3, "should have variable"
    assert 'violoncello_two_first_mov' in test_ins2_1, "should have variable"
    assert 'violoncello_two_second_mov' in test_ins2_2, "should have variable"
    assert '\\clef "bass"' in test_ins2_2, "should have clef"
    assert 'violoncello_two_third_mov' in test_ins2_3, "should have variable"
    assert 'piano_first_mov_RH' in piano_1
    assert 'piano_first_mov_LH' in piano_1
    assert '\\clef "treble"' in piano_1
    assert '\\clef "bass"' in piano_1
    assert 'piano_second_mov_RH' in piano_2
    assert 'piano_second_mov_LH' in piano_2
    assert 'piano_third_mov_RH' in piano_3
    assert 'piano_third_mov_LH' in piano_3


def test_includes(tmpdir, jinja_env, piece1):
    """Test the includes template."""
    template = jinja_env.get_template('includes.ily')
    extra_includes = [Path('expressions.ily'), Path('macros.ily')]
    includepaths = [Path('global', 'global_1.ily'),
                    Path('global', 'global_2.ily'),
                    Path('global', 'global_3.ily'),
                    Path('violin1', 'violin1_1.ily'),
                    Path('violin1', 'violin1_2.ily'),
                    Path('violin1', 'violin1_3.ily'),
                    ]
    render = template.render(piece=piece1, extra_includes=extra_includes,
                             includepaths=includepaths)

    with open(Path(tmpdir, 'includes.ily'), 'w') as file1:
        file1.write(render)

    with open(Path(tmpdir, 'includes.ily'), 'r') as file2:
        test_render1 = file2.read()

    assert 'Path' not in test_render1,\
        'path objects should come out as strings'
    assert 'Test Piece' in test_render1, 'Name of piece should be in comment'
    assert '\\include "violin1/violin1_1.ily"' in test_render1,\
        'path should assemble from path object'
    assert '\\version "2.' in test_render1, 'version number should be in file'
    assert '\\include "global/global_2.ily"' in test_render1,\
        'path should assemble for global'


def test_score(piece1, jinja_env, instrument_list1, piano, tmpdir):
    """Test the score template."""
    instruments = instrument_list1.append(piano)
    lyglobal = lynames.LyName(name='global')
    template = jinja_env.get_template('score.ly')
    render = template.render(piece=piece1, filename='score.ly',
                             lyglobal=lyglobal, instruments=instrument_list1)
    scorepath = Path(tmpdir, 'score.ly')
    with open(scorepath, 'w') as scorefile:
        scorefile.write(render)

    with open(scorepath, 'r') as scorefile:
        scorerender = scorefile.read()

    assert 'Test Piece' in scorerender
    assert '\\version' in scorerender
    assert '\\violin_one_first_mov' in scorerender
    assert '\\global_first_mov' in scorerender
    assert '\\violoncello_two_third_mov' in scorerender
    assert '\\piano_first_mov_LH' in scorerender
    assert 'shortInstrumentName = "Cl."' in scorerender
    assert 'instrumentName = "Violin I"' in scorerender
