import SOAPpy
from bs4 import BeautifulSoup
from queue.models import ConfluenceSettings

confluence_settings = ConfluenceSettings.objects.all()[0]
soap = SOAPpy.WSDL.Proxy(confluence_settings.url)


def get_statistics():
    page_title = confluence_settings.page_title
    html = __get_page_html(page_title)
    data_sets = __parse_html_to_data_sets(html)
    lines = __get_array_of_table_rows_from_data_sets(data_sets)
    return __count_statistics(lines)


class TableRecord:
    def __init__(self, html_line):
        self.story_number = html_line[0][1]
        self.status = html_line[1][1]
        self.ba = html_line[2][1]
        self.comments = html_line[3][1]
        self.date = html_line[4][1]


def __get_page_from_confluence(page_title):
    auth = soap.login(confluence_settings.login, confluence_settings.password)
    page = soap.getPage(auth, confluence_settings.namespace, page_title)
    return page


def __get_page_html(page_title):
    page = __get_page_from_confluence(page_title)
    html = page.content
    return html


def __parse_html_to_data_sets(html):
    soup = BeautifulSoup(html)
    table = soup.find("table")
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    data_sets = []
    for row in table.find_all("tr")[1:]:
        data_set = zip(headings, (td.get_text() for td in row.find_all("td")))
        data_sets.append(data_set)

    return data_sets


def __get_array_of_table_rows_from_data_sets(data_sets):
    lines = []
    for item in data_sets:
        lines.append(TableRecord(item))
    return lines


def __count_statistics(lines):
    all_items = lines
    passed = []
    ready = []
    failed = []
    other = []

    for item in all_items:
        if item.status == 'Pass':
            passed.append(item)
        elif item.status == 'Ready':
            ready.append(item)
        elif item.status == 'Failed':
            failed.append(item)
        else:
            other.append(item)

    total = len(all_items)
    return {
        'total': {
            'count': total
        },
        'other': {
            'count': len(other),
            'percent': round(100.0 * len(other) / total, 1)
        },
        'passed': {
            'count': len(passed),
            'percent': round(100.0 * len(passed) / total, 1)
        },
        'ready': {
            'count': len(ready),
            'percent': round(100.0 * len(ready) / total, 1)
        },
        'failed': {
            'count': len(failed),
            'percent': round(100.0 * len(failed) / total, 1)
        }
    }

