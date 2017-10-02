"""Test the render functions."""
import os
from pathlib import Path
import pytest
from lyskel import render
from lyskel import lynames


def test_make_instrument(test_ins, test_ins2, test_ins3, piece1, piece2,
                         tmpdir):
    """Test making the files and directory for an instrument."""
    lyglobal = lynames.LyName('global')
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
