from queue.models import OutdatedJiraIssue, DeskCheckStatistic
from queue.rpc_util import jira_rpc_init, confluence_rpc_init
from queue.jira import JiraIssue, CanbanCard
from SOAPpy import Types
from bs4 import BeautifulSoup
from datetime import datetime
from dpq.settings import MEDIA_ROOT
from queue.logger import LOGGER
from queue.jira import jira_settings, AdvancedSearchRequest
import xlwt
import re


class ConfluenceDeskCheckUtil(object):
    class TableRecord:
        def __init__(self, html_line):
            self.story_number = html_line[0][1].strip()
            self.status = html_line[1][1].strip()
            self.ba = html_line[2][1]
            self.comments = html_line[3][1]
            self.date = html_line[4][1]
            self.sp = 0

    @staticmethod
    def get_statistics():
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

    @staticmethod
    def save_statistics():
        html = ConfluenceDeskCheckUtil.get_confluence_page_content()
        data_sets = ConfluenceDeskCheckUtil.html_to_data_sets(html)
        table_records = ConfluenceDeskCheckUtil.data_sets_to_table_records(data_sets)
        ConfluenceDeskCheckUtil.save_tabe_records_to_database(table_records)

    @staticmethod
    def save_tabe_records_to_database(table_records):
        all_items = table_records
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
                LOGGER.info('Story {key} is not estimated'.format(key=item.story_number))
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

    @staticmethod
    def data_sets_to_table_records(data_sets):

        table_records = {}
        issue_key_list = []
        for item in data_sets:
            record = ConfluenceDeskCheckUtil.TableRecord(item)
            key = record.story_number.encode('ascii', 'ignore')
            table_records[key] = record
            issue_key_list.append(key)

        issues = JiraUtil.get_issues(issue_key_list)

        result = []
        for issue in issues:
            record = table_records[issue.key]
            if issue.story_points:
                record.sp = int(issue.story_points)
            else:
                record.sp = 0
            result.append(record)
        return result

    @staticmethod
    def html_to_data_sets(html):
        soup = BeautifulSoup(html)
        table = soup.find("table")
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        data_sets = []
        for row in table.find_all("tr")[1:]:
            data_set = zip(headings, (td.get_text() for td in row.find_all("td")))
            data_sets.append(data_set)

        LOGGER.info('Page contains {count} data sets'.format(count=len(data_set)))
        return data_sets

    @staticmethod
    def get_confluence_page_content():
        env = confluence_rpc_init(LOGGER)
        auth = env['auth']
        client = env['client']
        namespace = env['namespace']
        page_title = env['page_title']

        LOGGER.info('Queuing Confluence for page with title {title}'.format(title=page_title))
        page = client.getPage(auth, namespace, page_title)

        html = page.content
        LOGGER.info('Confluence returned {size} bytes of html data'.format(size=len(html)))
        return html


class JiraUtil(object):

    @staticmethod
    def get_issues(key_list):
        normalized_keys = []
        for key in key_list:
            normalized_keys.append(key.encode('ascii', 'ignore'))
        issue_key_list = re.sub(r'[\[\]]', '', str(normalized_keys))
        request = '''project={project} AND key in ({list})'''.format(project=jira_settings.project_name,
                                                                     list=issue_key_list)
        search_request = AdvancedSearchRequest(request)
        search_request.request()
        response = search_request.get_response()

        return JiraUtil.__raw_data_to_issues_list__(response)

    @staticmethod
    def store_outdated_issues():
        env = jira_rpc_init(LOGGER)
        client = env['client']
        auth = env['auth']
        project_name = env['project_name']

        request = '''Sprint in openSprints() AND project = {project}
            AND type in (Story, Bug, Improvement)
            AND "Estimation Date" <= endOfDay()'''.format(project=project_name)

        LOGGER.info('Queuing JIRA for outdated issues...')
        response = client.getIssuesFromJqlSearch(auth, request, Types.intType(20))
        LOGGER.info('Response contains {count} issues'.format(count=len(response)))

        LOGGER.info('Removing all outdated issues from database...')
        OutdatedJiraIssue.objects.all().delete()

        LOGGER.info('Starting to import issues to database...')
        for issue in JiraUtil.__raw_data_to_issues_list__(response):
            message = '\tIssue {key} is being saved in database'.format(key=issue.key)
            LOGGER.info(message)

            outdated_jira_issue = JiraUtil.get_filled_in_outdated_jira_issue_obj(issue)
            outdated_jira_issue.save()

    @staticmethod
    def get_filled_in_outdated_jira_issue_obj(issue):
        return OutdatedJiraIssue.objects.get_or_create(
            key=issue.key,
            summary=issue.summary,
            description=issue.description,
            assignee=issue.assignee,
            tester=issue.tester,
            reporter=issue.reporter,
            points=issue.story_points,
            epic=issue.epic_key,
            team=issue.team,
            is_deskcheck=issue.desk_check,
            estimation_date=issue.estimation_date
        )[0]

    @staticmethod
    def get_outdated_issues():
        return OutdatedJiraIssue.objects.all().order_by('estimation_date')

    @staticmethod
    def __raw_data_to_issues_list__(raw_data):
        result = []
        for item in raw_data:
            issue = JiraIssue(item)
            result.append(issue)
        return result


class CanbanCardsUtil(object):
    @staticmethod
    def generate_cards(key_list):
        issues = JiraUtil.get_issues(key_list)
        result = []
        for index, issue in enumerate(issues):
            card = CanbanCard(issue, index)
            result.append(card)
        return result

    @staticmethod
    def save_cards_to_file(cards):
        out_file = xlwt.Workbook()
        prefix = 'Cards'
        sheet_name = CanbanCardsUtil.__generate_sheet_name__(prefix)
        sheet = out_file.add_sheet(sheet_name)

        for card in cards:
            sheet = card.render(sheet)

        sheet.write_merge(r1=0, c1=0, r2=0, c2=6, label='DeskCheck stories are marked with green colour.')

        filename, path = CanbanCardsUtil.__generate_file_name__(prefix)
        out_file.save(path + filename)
        return filename

    @staticmethod
    def __generate_sheet_name__(prefix):
        now = datetime.now()
        sheet_name = '{prefix} {datetime}'.format(prefix=prefix,
                                                  datetime=now.strftime("%Y.%m.%d %H-%M-%S"))
        return sheet_name

    @staticmethod
    def __generate_file_name__(prefix):
        now = datetime.now()
        file_name = '{prefix}_{datetime}.xls'.format(prefix=prefix, datetime=now.strftime("%Y.%m.%d_%H-%M-%S"))
        path = '{media_root}/cards/'.format(media_root=MEDIA_ROOT)
        return file_name, path
