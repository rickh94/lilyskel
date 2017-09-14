"""Tests that template files produce the correct output."""
import os
from pathlib import Path
import pytest
from jinja2 import Environment, PackageLoader
from lyskel import info
from lyskel import lynames


@pytest.fixture
def jinja_env():
    """Defines a jinja environment loading the default templates."""
    return Environment(
        loader=PackageLoader('lyskel', 'templates')
    )


@pytest.fixture
def mov_one_all():
    """Populated first movement."""
    return info.Movement(num=1,
                         tempo='Allegro',
                         time='4/4',
                         key=('a', 'major'))


@pytest.fixture
def mov_one_empty():
    """Empty first movement."""
    return info.Movement(num=1)


@pytest.fixture
def mov_two():
    """Two movement."""
    return info.Movement(num=2,
                         tempo='Largo',
                         key=('a', 'minor'),
                         time='3/4'
                         )


@pytest.fixture
def mov_three():
    """Third movement"""
    return info.Movement(num=3,
                         tempo='Vivace',
                         key=('a', 'major'),
                         time='2/4'
                         )


@pytest.fixture
def mov_four():
    """fourth movement"""
    return info.Movement(num=4,
                         tempo='Adagio',
                         key=('d', 'major')
                         )


@pytest.fixture
def mov_five():
    """blank movement"""
    return info.Movement(num=5)


@pytest.fixture
def mov_six():
    """blank movement"""
    return info.Movement(num=6)


@pytest.fixture
def three_movs(mov_one_all, mov_two, mov_three):
    """Three movements."""
    return [mov_one_all, mov_two, mov_three]


@pytest.fixture
def piece1(headers1, three_movs):
    """A piece with minimal headers."""
    return info.Piece.init_version(name='testpiece1',
                                   language='english',
                                   headers=headers1,
                                   movements=three_movs
                                   )


@pytest.fixture
def six_movs(mov_one_empty, mov_two, mov_three, mov_four, mov_five, mov_six):
    """List of six movements."""
    return [mov_one_empty, mov_two, mov_three, mov_four, mov_five, mov_six]


@pytest.fixture
def piece2(headers2, six_movs):
    """A piece with more complete headers."""
    return info.Piece.init_version(name='testpiece2',
                                   language='english',
                                   headers=headers2,
                                   opus='Op. 15',
                                   movements=six_movs
                                   )


def test_render_defs(tmpdir, jinja_env, piece1, piece2):
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


def test_render_ins_part(tmpdir, jinja_env, test_ins, test_ins3, piece1,
                         piece2):
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
    moreincludes = ['expressions.ily']
    render1 = instemplate.render(piece=piece1, instrument=test_ins,
                                 lyglobal=lyglobals, flags=flags1,
                                 moreincludes=moreincludes,
                                 filename='inspart_test1.ly')
    render2 = instemplate.render(piece=piece2, instrument=test_ins3,
                                 lyglobal=lyglobals, flags=flags2,
                                 filename='inspart_test2.ly')
    with open(Path(tmpdir, 'inspart_test1.ly'), 'w') as part:
        part.write(render1)

    with open(Path(tmpdir, 'inspart_test2.ly'), 'w') as part:
        part.write(render2)

    with open(Path(tmpdir, 'inspart_test1.ly'), 'r') as part:
        part_test1 = part.read()

    with open(Path(tmpdir, 'inspart_test2.ly'), 'r') as part:
        part_test2 = part.read()

    assert 'expressions.ily' in part_test1
    assert '\\version' in part_test1
    assert '\\include "defs.ily"' in part_test1
    assert '\\violin_one_first_mov' in part_test1
    assert '\\global_second_mov' in part_test1
    assert '\\compressFullBarRests' in part_test1
    assert '\\key a \\major' in part_test1
    assert '\\key a \\minor' in part_test1
    assert '\\time 4/4' in part_test1

    assert '\\version' in part_test2
    assert '\\include "defs.ily"' in part_test2
    assert '\\clarinet_in_bb_first_mov' in part_test2
    assert '\\clarinet_in_bb_fourth_mov' in part_test2
    assert '\\global_second_mov' in part_test2
    assert '\\compressFullBarRests' not in part_test2
    assert 'Op. 15' in part_test2
    assert '\\key c \\major' in part_test2
    assert '\\time 3/4' in part_test2


@pytest.fixture
def global_ins():
    """An object for global info."""
    return lynames.LyName(name='global')


def test_render_notes(tmpdir, jinja_env, test_ins, test_ins2, three_movs,
                      piece1, global_ins):
    """Test generating the notes template parts."""
    template = jinja_env.get_template('notes.ily')
    for ins in [global_ins, test_ins, test_ins2]:
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

    assert 'global_first_mov' in global1, "should have variable"
    assert 'Allegro' in global1, "global should have tempo"
    assert 'global_second_mov' in global2, "should have variable"
    assert 'global_third_mov' in global3, "should have variable"
    assert 'violin_one_first_mov' in test_ins_1, "should have variable"
    assert 'violin_one_second_mov' in test_ins_2, "should have variable"
    assert 'violin_one_third_mov' in test_ins_3, "should have variable"
    assert 'violoncello_two_first_mov' in test_ins2_1, "should have variable"
    assert 'violoncello_two_second_mov' in test_ins2_2, "should have variable"
    assert 'violoncello_two_third_mov' in test_ins2_3, "should have variable"
