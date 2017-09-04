"""Tests that template files produce the correct output."""
from pathlib import Path
import pytest
from jinja2 import Environment, PackageLoader
from lyskel import info


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
    defstemplate = jinja_env.get_template('defs.ly')
    with open(Path(tmpdir, 'defs_test1.ly'), 'w') as defs1:
        defs1.write(defstemplate.render(piece=piece1))
    with open(Path(tmpdir, 'defs_test2.ly'), 'w') as defs2:
        defs2.write(defstemplate.render(piece=piece2))

    with open(Path(tmpdir, 'defs_test1.ly'), 'r') as defs1:
        test1 = defs1.read()
    with open(Path(tmpdir, 'defs_test2.ly'), 'r') as defs2:
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
