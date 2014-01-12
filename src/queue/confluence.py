import SOAPpy
from bs4 import BeautifulSoup
from queue.models import ConfluenceSettings, DeskCheckStatistic
from jira import *
from utils import log_info

confluence_settings = ConfluenceSettings.objects.all()[0]
soap = SOAPpy.WSDL.Proxy(confluence_settings.url)


def get_statistics():
    return __get_formatted_statistics__()


def store_statistics():
    page_title = confluence_settings.page_title
    html = __get_page_html(page_title)
    data_sets = __parse_html_to_data_sets(html)
    lines = __get_array_of_table_rows_from_data_sets(data_sets)
    return __save_statistics_to_database(lines)


class TableRecord:
    def __init__(self, html_line):
        self.story_number = html_line[0][1].strip()
        self.status = html_line[1][1].strip()
        self.ba = html_line[2][1]
        self.comments = html_line[3][1]
        self.date = html_line[4][1]
        self.sp = 0


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
    auth = get_auth()
    for item in data_sets:
        record = TableRecord(item)
        try:
            record.sp = int(JIRAStory(record.story_number, 0, auth).points)
        except AttributeError:
            record.sp = 0
        lines.append(record)
    return lines


def __save_statistics_to_database(lines):
    all_items = lines
    passed = []
    ready = []
    failed = []
    other = []
    total_sp = 0
    passed_sp = 0
    ready_sp = 0
    failed_sp = 0
    other_sp = 0

    for item in all_items:
        skip = False
        try:
            total_sp += item.sp
        except TypeError:
            skip = True
            log_info('Story {key} is not estimated'.format(key=item.story_number))
        if item.status == 'Pass':
            passed.append(item)
            if not skip:
                passed_sp += item.sp
        elif item.status == 'Ready':
            ready.append(item)
            if not skip:
                ready_sp += item.sp
        elif item.status == 'Failed':
            failed.append(item)
            if not skip:
                failed_sp += item.sp
        else:
            other.append(item)
            if not skip:
                other_sp += item.sp

    total = len(all_items)

    passed_count = len(passed)
    passed_percent = round(100.0 * len(passed) / total, 0)
    passed_percent_sp = round(100.0 * passed_sp / total_sp, 0)
    ready_count = len(ready)
    ready_percent = round(100.0 * len(ready) / total, 0)
    ready_percent_sp = round(100.0 * ready_sp / total_sp, 0)
    failed_count = len(failed)
    failed_percent = round(100.0 * len(failed) / total, 0)
    failed_percent_sp = round(100.0 * failed_sp / total_sp, 0)

    other_count = len(other)
    other_percent = 100 - passed_percent - ready_percent - failed_percent
    other_percent_sp = 100 - passed_percent_sp - ready_percent_sp - failed_percent_sp

    db_item = DeskCheckStatistic(
        total_count=total,
        total_count_sp=total_sp,
        other_count=other_count,
        other_count_sp=other_sp,
        other_percent=other_percent,
        other_percent_sp=other_percent_sp,
        passed_count=passed_count,
        passed_count_sp=passed_sp,
        passed_percent=passed_percent,
        passed_percent_sp=passed_percent_sp,
        ready_count=ready_count,
        ready_count_sp=ready_sp,
        ready_percent=ready_percent,
        ready_percent_sp=ready_percent_sp,
        failed_count=failed_count,
        failed_count_sp=failed_sp,
        failed_percent=failed_percent,
        failed_percent_sp=failed_percent_sp
    )
    db_item.save()


def __get_formatted_statistics__():
    db_item = DeskCheckStatistic.objects.all().order_by('-creation_date')[0]
    return {
        'datetime': db_item.creation_date,
        'total': {
            'count': int(db_item.total_count),
            'count_sp': int(db_item.total_count_sp)
        },
        'other': {
            'count': int(db_item.other_count),
            'count_sp': int(db_item.other_count_sp),
            'percent': int(db_item.other_percent),
            'percent_sp': int(db_item.other_percent_sp)
        },
        'passed': {
            'count': int(db_item.passed_count),
            'count_sp': int(db_item.passed_count_sp),
            'percent': int(db_item.passed_percent),
            'percent_sp': int(db_item.passed_percent_sp)
        },
        'ready': {
            'count': int(db_item.ready_count),
            'count_sp': int(db_item.ready_count_sp),
            'percent': int(db_item.ready_percent),
            'percent_sp': int(db_item.ready_percent_sp)
        },
        'failed': {
            'count': int(db_item.failed_count),
            'count_sp': int(db_item.failed_count_sp),
            'percent': int(db_item.failed_percent),
            'percent_sp': int(db_item.failed_percent_sp)
        },
        'progressbar': {
            'passed': int(db_item.passed_percent),
            'ready': int(db_item.ready_percent),
            'other': int(db_item.failed_percent + db_item.other_percent)
        }
    }

