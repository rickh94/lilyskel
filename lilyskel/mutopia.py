"""Functions for scraping mutopia info."""
import requests
from bs4 import BeautifulSoup
from lilyskel import exceptions

SITE = None
SITE2 = None
LICENSES = None
COMPOSERS = None
INSTRUMENTS = None


def _scrape_mutopia():
    """Grab the table off mutopia contributing."""
    # pylint: disable=global-statement
    global SITE
    if not SITE:
        SITE = requests.get("http://www.mutopiaproject.org/contribute.html")
    site_html = BeautifulSoup(SITE.content, 'html.parser')
    return site_html.table.find_all('td')


def _get_mutopia_table_data(field):
    """Get data out of the mutopia contributing table."""
    table = _scrape_mutopia()
    for index, item in enumerate(table):
        if field in item.get_text():
            return table[index + 1]
    raise exceptions.MutopiaError("'{field}' was not found".format(
        field=field))


def validate_mutopia(field, data):
    """Validates mutopia fields against accepted mutopia input."""
    # special case for licenses
    if field == 'license':
        licenses = _get_licenses()
        if data not in licenses:
            raise exceptions.MutopiaError(
                '{data} was not found in {field}'.format(data=data,
                                                         field=field))
        else:
            return

    text = _get_mutopia_table_data(field=field)
    # this will clean out some preceding text
    breaktext = text.get_text().split(':\n')
    cleantext = breaktext[1]
    data_list = [item.strip() for item in cleantext.split(', ')]
    if data not in data_list:
        raise exceptions.MutopiaError(f'{data} was not found in {field}')


def _get_licenses():
    """Gets allowed licenses from mutopia.org and returns a list."""
    global LICENSES
    if LICENSES:
        return LICENSES
    text = _get_mutopia_table_data(field='license')
    licenses = text.find_all('li')
    # some text cleaning
    LICENSES = [license.get_text().replace('"', '') for license in licenses]
    return LICENSES


def _get_composers():
    """Gets allowed licenses from mutopia.org and returns a list."""
    global COMPOSERS
    if COMPOSERS:
        return COMPOSERS
    text = _get_mutopia_table_data(field='mutopiacomposer')
    breaktext = text.get_text().split(':\n')
    cleantext = breaktext[1]
    COMPOSERS = [item.strip() for item in cleantext.split(', ')]
    # some text cleaning
    return COMPOSERS


def _get_instruments():
    """Gets the allowed instruments from mutopia."""
    global INSTRUMENTS
    if INSTRUMENTS:
        return INSTRUMENTS
    global SITE2
    if not SITE2:
        SITE2 = requests.get("http://www.mutopiaproject.org/advsearch.html")
    html = BeautifulSoup(SITE2.content, 'html.parser')
    inst_elements = html.find(id='adv-instr-sel')
    INSTRUMENTS = []
    for item in inst_elements.find_all('option'):
        INSTRUMENTS.append(item['value'])
    return INSTRUMENTS
