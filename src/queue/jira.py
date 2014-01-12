import SOAPpy
import re
from dpq.settings import *
from queue.models import JiraSettings, OutdatedJiraIssue
import datetime
from xlwt_styles import *

soap = SOAPpy.WSDL.Proxy(JIRA_URL)
jira_settings = JiraSettings.objects.all()[0]


class JIRAStory:
    def __init__(self, index, key, summary, description, assignee, tester, reporter, points, epic, team=''):
        self.row = index / 2 * 15
        self.column = (6, 0)[index % 2 == 0]
        self.key = key
        self.summary = summary
        self.description = description
        self.assignee = assignee
        self.tester = tester
        self.reporter = reporter
        self.points = points
        self.epic = epic
        self.team = team
        self.is_deskcheck = False

    @staticmethod
    def __parse_custom_fields__(node):
        sp = "n/a"
        epic_key = None
        tester = None
        is_deskcheck = False

        for i in range(1, len(node) + 1):
            try:
                if node[i].customfieldId in STORY_POINTS_CUSTOM_FIELDS:
                    sp = node[i].values[0]
                    continue
                elif node[i].customfieldId in EPIC_NAME_CUSTOM_FIELDS:
                    epic_key = node[i].values[0]
                    continue
                elif node[i].customfieldId in TESTER_CUSTOM_FIELDS:
                    tester = node[i].values[0]
                    continue
                elif node[i].customfieldId in TEAM_CUSTOM_FIELDS:
                    team = node[i].values[0]
                    continue
                elif node[i].customfieldId in DESK_CHECK_CUSTOM_FIELDS:
                    if node[i].values[0] == "Yes":
                        is_deskcheck = True
                    continue
                else:
                    continue
            except IndexError:
                break
        return epic_key, sp, tester, is_deskcheck, team

    @staticmethod
    def __format_description__(description):
        return (description, description[:127] + ' ...')[len(description) > 128]

    @staticmethod
    def __remove_underscores__(field):
        return (re.sub('_', ' ', str(field)), 'not assigned')[field is None]

    def __init__(self, key, index, auth):
        self.row = index / 2 * 15
        self.column = (6, 0)[index % 2 == 0]

        try:
            issue = soap.getIssue(auth, key)
            self.success = True
        except:
            issue = None
            self.success = False

        if issue:
            epic_key, story_points, tester, is_deskcheck, team = self.__parse_custom_fields__(issue[5])

            if epic_key is not None:
                epic = soap.getIssue(auth, epic_key)
                self.epic = epic.summary
            else:
                self.epic = "n/a"

            self.description = self.__format_description__(issue.description)
            self.assignee = self.__remove_underscores__(issue.assignee)
            self.reporter = self.__remove_underscores__(issue.reporter)
            self.tester = self.__remove_underscores__(tester)
            self.key = issue.key
            self.summary = issue.summary
            self.points = story_points
            self.is_deskcheck = is_deskcheck
            self.team = team

    def render(self, sheet):

        # Story number
        self.key = re.sub(PROJECT_NAME + '-', '', self.key)

        if self.is_deskcheck:
            key_style = STORY_KEY_STYLE_DESK_CHECK
        else:
            key_style = STORY_KEY_STYLE

        sheet.write_merge(r1=self.row+1, c1=self.column+0,
                          r2=self.row+4, c2=self.column+0,
                          label=self.key, style=key_style)

        #Summary
        sheet.write_merge(r1=self.row+1, c1=self.column+1,
                          r2=self.row+4, c2=self.column+5,
                          label=self.summary, style=SUMMARY_STYLE)

        #Description
        sheet.write_merge(r1=self.row+5, c1=self.column+0,
                          r2=self.row+11, c2=self.column+5,
                          label=self.description, style=DESCRIPTION_STYLE)

        #Assignee
        sheet.write_merge(r1=self.row+12, c1=self.column+0,
                          r2=self.row+12, c2=self.column+1,
                          label="Assignee:", style=ASSIGNEE_LABEL_STYLE)
        sheet.write_merge(r1=self.row+12, c1=self.column+2,
                          r2=self.row+12, c2=self.column+4,
                          label=self.assignee, style=ASSIGNEE_STYLE)

        #Tester
        sheet.write_merge(r1=self.row+13, c1=self.column+0,
                          r2=self.row+13, c2=self.column+1,
                          label="Tester:", style=TESTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+13, c1=self.column+2,
                          r2=self.row+13, c2=self.column+4,
                          label=self.tester, style=TESTER_STYLE)

        #Reporter
        sheet.write_merge(r1=self.row+14, c1=self.column+0,
                          r2=self.row+14, c2=self.column+1,
                          label="Reporter:", style=REPORTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+14, c1=self.column+2,
                          r2=self.row+14, c2=self.column+4,
                          label=self.reporter, style=REPORTER_STYLE)

        #Story points
        sheet.write_merge(r1=self.row+12, c1=self.column+5,
                          r2=self.row+14, c2=self.column+5,
                          label=self.points, style=STORY_POINTS_STYLE)

        #Epic
        sheet.write_merge(r1=self.row+15, c1=self.column+0,
                          r2=self.row+15, c2=self.column+5,
                          label=self.epic, style=EPIC_STYLE)

        return sheet


def fetch_story(key):
    auth = get_auth()
    return JIRAStory(key, 0, auth)


def get_stories_from_list(list):
    result = []
    auth = get_auth()
    for index, story_number in enumerate(list):
        result.append(JIRAStory(story_number, index, auth))
    return result


def render_cards(cards):
    out_file = xlwt.Workbook()
    sheet = out_file.add_sheet(get_sheet_name('Cards'))

    for card in cards:
        sheet = card.render(sheet)

    sheet.write_merge(r1=0, c1=0, r2=0, c2=6, label='DeskCheck stories are marked with green colour.')

    filename, path = get_cards_filename()
    out_file.save(path+filename)
    return filename


def get_sheet_name(prefix):
    now = datetime.datetime.now()
    sheet_name = '{prefix} {datetime}'.format(prefix=prefix,
                                              datetime=now.strftime("%Y.%m.%d %H-%M-%S"))
    return sheet_name


def get_cards_filename():
    now = datetime.datetime.now()
    return 'Cards_' + now.strftime("%Y.%m.%d_%H-%M-%S") + '.xls', MEDIA_ROOT + '/cards/'


def get_auth():
    return soap.login(JIRA_LOGIN, JIRA_PASSWORD)


def get_outdated_issues():
    return OutdatedJiraIssue.objects.all()


def store_outdated_issues():
    project_name = unicode(jira_settings.project_name)
    auth = get_auth()
    request = '''Sprint in openSprints() AND project = {project}
        AND type in (Story, Bug, Improvement)
        AND "Estimation Date" < endOfDay()'''.format(project=project_name)
    issues = soap.getIssuesFromJqlSearch(auth, request, SOAPpy.Types.intType(20))

    OutdatedJiraIssue.objects.all().delete()

    for issue in issues:
        jira_issue = JIRAStory(issue.key, 0, auth)
        db_issue = OutdatedJiraIssue.objects.get_or_create(key=issue.key)[0]
        db_issue.summary = jira_issue.summary
        db_issue.description = jira_issue.description
        db_issue.assignee = jira_issue.assignee
        db_issue.tester = jira_issue.tester
        db_issue.reporter = jira_issue.reporter
        db_issue.points = jira_issue.points
        db_issue.epic = jira_issue.epic
        db_issue.team = jira_issue.team
        db_issue.is_deskcheck = jira_issue.is_deskcheck

        db_issue.save()
