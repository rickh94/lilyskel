"""Tests for functions scraping mutopia."""
import pytest
from lyskel import mutopia
from lyskel import exceptions
# pylint: disable=protected-access


def test_scrape_mutopia():
    """Test mutopia scraping."""
    tabledata = mutopia._scrape_mutopia()
    sitefirstrun = mutopia.SITE
    for item in tabledata:
        assert 'td' in str(item),\
           "Should only return td elements from the table."
    mutopia._scrape_mutopia()
    assert sitefirstrun is mutopia.SITE, ("One downloaded, the site should set"
                                          " the SITE global and not download "
                                          "again.")


def test_get_mutopia_table_data():
    """Test getting data from the table."""
    data1 = mutopia._get_mutopia_table_data('style')
    assert 'Baroque' in data1.get_text(), "This should contain the styles."
    data2 = mutopia._get_mutopia_table_data('license')
    assert 'Creative Commons' in data2.get_text(),\
        "This should contain the licenses"
    data3 = mutopia._get_mutopia_table_data('mutopiacomposer')
    assert 'BachJS' in data3.get_text(), "This should contain the composers"

    with pytest.raises(exceptions.MutopiaError, match='.* was not found',
                       message=('Expect MutopiaError if the field is not found'
                                ' in the table.')):
        mutopia._get_mutopia_table_data('nonexistent')


def test_validate_mutopia():
    """Test validating the mutopia data."""
    # These should simply not raise exceptions
    mutopia.validate_mutopia(field='mutopiacomposer', data='BachJS')
    mutopia.validate_mutopia(field='style', data='Classical')
    mutopia.validate_mutopia(field='license',
                             data='Creative Commons Attribution 4.0')

    with pytest.raises(exceptions.MutopiaError, match='.*was not found in.*',
                       message=('if the data is invalid, it should raise '
                                'MutopiaError.')):
        mutopia.validate_mutopia(field='mutopiacomposer', data='josiopih')

    with pytest.raises(exceptions.MutopiaError, match='.*was not found in.*',
                       message=('if the data is invalid, it should raise '
                                'MutopiaError.')):
        mutopia.validate_mutopia(field='style', data='fjsioiue')
    with pytest.raises(exceptions.MutopiaError, match='.*was not found in.*',
                       message=('if the data is invalid, it should raise '
                                'MutopiaError.')):
        mutopia.validate_mutopia(field='license', data='Creatmutopiaive')


def test_get_licenses():
    """Test getting the licenses."""
    licenses = {"Creative Commons Attribution 4.0",
                "Creative Commons Attribution-ShareAlike 4.0",
                "Public Domain"}
    assert licenses.issubset(set(mutopia._get_licenses())),\
        "These licenses should be in the list, and possibly more."


def test_get_composers():
    """Test getting list of mutopia formatted composers."""
    assert {'BachJS', 'BeethovenLv', 'HolstGT', 'TchaikovskyPI',
            'Anonymous', 'Traditional'}.issubset(
                set(mutopia._get_composers()))


def test_get_instruments():
    """Test getting list of instruments from mutopia."""
    assert {'Violin', 'Cello', 'Flute', 'Clarinet', 'Trumpet'}.issubset(
        set(mutopia._get_instruments())),\
        "These instruments are allowed and should be in the list."
