import SOAPpy
import re
from dpq.settings import *
import datetime
import xlwt
from xlwt_styles import *

soap = SOAPpy.WSDL.Proxy(JIRA_URL)


class JIRAStory:
    def __init__(self, index, key, summary, description, assignee, tester, reporter, points, epic):
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

    def __parse_custom_fields(self, node):
        sp = "n/a"
        epic_key = None
        tester = None

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
                else:
                    continue
            except IndexError:
                break
        return epic_key, sp, tester

    def __format_description(self, description):
        return (description, description[:127] + ' ...')[len(description) > 128]

    def __remove_underscores(self, field):
        return (re.sub('_', ' ', str(field)), 'not assigned')[field is None]

    def __init__(self, key, index):
        self.row = index / 2 * 15
        self.column = (6, 0)[index % 2 == 0]
        auth = soap.login(JIRA_LOGIN, JIRA_PASSWORD)

        try:
            issue = soap.getIssue(auth, key)
            self.success = True
        except:
            issue = None
            self.success = False

        if issue:
            epic_key, story_points, tester = self.__parse_custom_fields(issue[5])

            if epic_key is not None:
                epic = soap.getIssue(auth, epic_key)
                self.epic = epic.summary
            else:
                self.epic = "n/a"

            self.description = self.__format_description(issue.description)
            self.assignee = self.__remove_underscores(issue.assignee)
            self.reporter = self.__remove_underscores(issue.reporter)
            self.tester = self.__remove_underscores(tester)
            self.key = issue.key
            self.summary = issue.summary
            self.points = story_points

    def render(self, sheet):

        # Story number
        self.key = re.sub(PROJECT_NAME + '-', '', self.key)
        sheet.write_merge(r1=self.row+0, c1=self.column+0,
                          r2=self.row+3, c2=self.column+0,
                          label=self.key, style=STORY_KEY_STYLE)

        #Summary
        sheet.write_merge(r1=self.row+0, c1=self.column+1,
                          r2=self.row+3, c2=self.column+5,
                          label=self.summary, style=SUMMARY_STYLE)

        #Description
        sheet.write_merge(r1=self.row+4, c1=self.column+0,
                          r2=self.row+10, c2=self.column+5,
                          label=self.description, style=DESCRIPTION_STYLE)

        #Assignee
        sheet.write_merge(r1=self.row+11, c1=self.column+0,
                          r2=self.row+11, c2=self.column+1,
                          label="Assignee:", style=ASSIGNEE_LABEL_STYLE)
        sheet.write_merge(r1=self.row+11, c1=self.column+2,
                          r2=self.row+11, c2=self.column+4,
                          label=self.assignee, style=ASSIGNEE_STYLE)

        #Tester
        sheet.write_merge(r1=self.row+12, c1=self.column+0,
                          r2=self.row+12, c2=self.column+1,
                          label="Tester:", style=TESTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+12, c1=self.column+2,
                          r2=self.row+12, c2=self.column+4,
                          label=self.tester, style=TESTER_STYLE)

        #Reporter
        sheet.write_merge(r1=self.row+13, c1=self.column+0,
                          r2=self.row+13, c2=self.column+1,
                          label="Reporter:", style=REPORTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+13, c1=self.column+2,
                          r2=self.row+13, c2=self.column+4,
                          label=self.reporter, style=REPORTER_STYLE)

        #Story points
        sheet.write_merge(r1=self.row+11, c1=self.column+5,
                          r2=self.row+13, c2=self.column+5,
                          label=self.points, style=STORY_POINTS_STYLE)

        #Epic
        sheet.write_merge(r1=self.row+14, c1=self.column+0,
                          r2=self.row+14, c2=self.column+5,
                          label=self.epic, style=EPIC_STYLE)

        return sheet


def fetch_story(key):
    return JIRAStory(key, 0)


def get_stories_from_list(list):
    result = []
    for index, story_number in enumerate(list):
        result.append(JIRAStory(story_number, index))
    return result


def render_cards(cards):
    out_file = xlwt.Workbook()
    sheet = out_file.add_sheet(get_sheet_name('Cards'))

    for card in cards:
        sheet = card.render(sheet)

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
