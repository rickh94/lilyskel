"""Functions for scraping mutopia info."""
import requests
from bs4 import BeautifulSoup
from lyskel import exceptions

SITE = None


def _scrape_mutopia():
    """Grab the table off mutopia contributing."""
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
            text = table[index + 1]
            break
    return text


def validate_mutopia(field, data):
    """Validates mutopia fields against accepted mutopia input."""
    # it's silly to download the site multiple times, so stick the content in a
    # global.
    text = _get_mutopia_table_data(field=field)
    if data not in text.get_text():
        raise exceptions.MutopiaError('{data} was not found in {field}'.format(
            data=data, field=field))


def _get_licenses():
    """Gets allowed licenses from mutopia.org and returns a list."""
    text = _get_mutopia_table_data(field='license')
    licenses = text.find_all('li')
    return [license.get_text() for license in licenses]
