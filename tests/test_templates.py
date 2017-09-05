"""Tests that template files produce the correct output."""
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
def piece1(headers1):
    """A piece with minimal headers."""
    return info.Piece.init_version(name='testpiece1',
                                   language='english',
                                   headers=headers1
                                   )


@pytest.fixture
def piece2(headers2):
    """A piece with more complete headers."""
    return info.Piece.init_version(name='testpiece2',
                                   language='english',
                                   headers=headers2
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


def test_render_ins_part(tmpdir, jinja_env, test_ins, piece1):
    """Tests rendering an instrument part."""
    instemplate = jinja_env.get_template('ins_part.ly')
    lyglobals = lynames.LyName(name='global')
    flags = {
        'key_in_partname': False,
        'compress_full_bar_rests': True,
    }
    moreincludes = ['expressions.ily']
    render1 = instemplate.render(piece=piece1, instrument=test_ins,
                                 lyglobal=lyglobals, flags=flags,
                                 movements=3, moreincludes=moreincludes)
    with open(Path(tmpdir, 'inspart_test1.ly'), 'w') as part:
        part.write(render1)

    with open(Path(tmpdir, 'inspart_test1.ly'), 'r') as part:
        part_test1 = part.read()

    assert 'expressions.ily' in part_test1
    assert '\\version' in part_test1
    assert '\\include "defs.ily"' in part_test1
    assert '\\violin_one_first_mov' in part_test1
    assert '\\global_second_mov' in part_test1
    assert '\\compressFullBarRests' in part_test1
