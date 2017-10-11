"""Test the render functions."""
import os
from pathlib import Path
import pytest
from lilyskel import render
from lilyskel import lynames


@pytest.fixture
def lyglobal():
    return lynames.LyName('global')


def test_make_instrument(test_ins, test_ins2, test_ins3, piece1, piece2,
                         tmpdir, lyglobal):
    """Test making the files and directory for an instrument."""
    test1_includes = render.make_instrument(
        instrument=test_ins, lyglobal=lyglobal, piece=piece1, location=tmpdir)
    test2_includes = render.make_instrument(
        instrument=test_ins2, lyglobal=lyglobal, piece=piece1, location=tmpdir)
    flags3 = {'key_in_partname': True, 'compress_full_bar_rests': True}
    test3_includes = render.make_instrument(
        instrument=test_ins3, lyglobal=lyglobal, piece=piece2, location=tmpdir)

    assert os.path.exists(Path(tmpdir, 'test_piece_violin1.ly'))
    assert os.path.exists(Path(tmpdir, 'violin1', 'violin1_1.ily'))
    assert os.path.exists(Path(tmpdir, 'violin1', 'violin1_2.ily'))
    assert os.path.exists(Path(tmpdir, 'violin1', 'violin1_3.ily'))
    assert Path('violin1', 'violin1_1.ily') in test1_includes

    assert os.path.exists(Path(tmpdir, 'test_piece_violoncello2.ly'))
    assert os.path.exists(Path(tmpdir, 'violoncello2', 'violoncello2_1.ily'))
    assert os.path.exists(Path(tmpdir, 'violoncello2', 'violoncello2_2.ily'))
    assert os.path.exists(Path(tmpdir, 'violoncello2', 'violoncello2_3.ily'))
    assert Path('violoncello2', 'violoncello2_2.ily') in test2_includes

    assert os.path.exists(Path(tmpdir, 'O15_clarinet_in_bb.ly'))
    assert os.path.exists(Path(tmpdir,
                               'clarinet_in_bb', 'clarinet_in_bb_1.ily'))
    assert os.path.exists(Path(tmpdir,
                               'clarinet_in_bb', 'clarinet_in_bb_2.ily'))
    assert os.path.exists(Path(tmpdir,
                               'clarinet_in_bb', 'clarinet_in_bb_3.ily'))
    assert Path('clarinet_in_bb', 'clarinet_in_bb_3.ily') in test3_includes


def test_render_includes(piece1, tmpdir):
    """Test rendering the include file."""
    includes = [
        Path('violin1', 'violin1_1.ily'),
        Path('violin1', 'violin1_2.ily'),
        Path('violin1', 'violin1_3.ily'),
    ]
    render.render_includes(includepaths=includes,
                           piece=piece1, location=tmpdir)
    assert os.path.exists(Path(tmpdir, 'includes.ily'))
    with open(Path(tmpdir, 'includes.ily'), 'r') as includefile:
        text = includefile.read()

    assert '\\include "violin1/violin1_1.ily"' in text
    assert '\\include "violin1/violin1_2.ily"' in text
    assert '\\include "violin1/violin1_3.ily"' in text


def test_render_defs(piece1, tmpdir):
    """Test rendering the defs file."""
    render.render_defs(piece=piece1, location=tmpdir)
    assert os.path.exists(Path(tmpdir, 'defs.ily'))
    with open(Path(tmpdir, 'defs.ily'), 'r') as defsfile:
        text = defsfile.read()

    assert '\\version "2.' in text
    assert '\\include "includes.ily"' in text
    assert 'title = "Test Piece"' in text


def test_render_score(piece1, instrument_list1, tmpdir, lyglobal):
    """Test rendering score file."""
    render.render_score(piece=piece1, instruments=instrument_list1,
                        lyglobal=lyglobal, path_prefix=tmpdir)
    scorepath = Path(tmpdir, 'test_piece_score.ly')
    assert scorepath.exists()
    with scorepath.open() as scorefile:
        text = scorefile.read()
    assert '\\version "2.' in text
    assert '\\book' in text
    assert '\\violin_one_first_mov' in text
    assert '\\global_third_mov' in text
    assert 'instrumentName = "Oboe"' in text
