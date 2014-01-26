import SOAPpy
import re
from queue.models import JiraSettings
from queue.rpc_util import setup_logging, jira_rpc_init
from time import strptime, mktime
from datetime import datetime
from xlwt_styles import *

jira_settings = JiraSettings.objects.all()[0]
log = setup_logging()

STORY_POINTS = jira_settings.custom_field_story_points
EPIC_NAME = jira_settings.custom_field_epic_name
TESTER = jira_settings.custom_field_tester
DESK_CHECK = jira_settings.custom_field_desk_check
TEAM = jira_settings.custom_field_team
ESTIMATION_DATE = jira_settings.custom_field_estimation_date


class CanbanCard(object):

    def __init__(self, issue, index):
        self.row = index / 2 * 15
        self.column = (6, 0)[index % 2 == 0]
        self.issue = issue

    def render(self, sheet):

        if self.issue.desk_check:
            key_style = STORY_KEY_STYLE_DESK_CHECK
        else:
            key_style = STORY_KEY_STYLE

        #Key
        project_name = re.sub('-', '', jira_settings.project_name)
        what = '{project_name}-'.format(project_name=project_name)
        key = re.sub(what, ' ', self.issue.key)
        sheet.write_merge(r1=self.row+1, c1=self.column+0,
                          r2=self.row+4, c2=self.column+0,
                          label=key, style=key_style)

        #Summary
        summary = self.issue.summary
        sheet.write_merge(r1=self.row+1, c1=self.column+1,
                          r2=self.row+4, c2=self.column+5,
                          label=summary, style=SUMMARY_STYLE)

        #Description
        description = self.__format_description__(self.issue.description)
        sheet.write_merge(r1=self.row+5, c1=self.column+0,
                          r2=self.row+11, c2=self.column+5,
                          label=description, style=DESCRIPTION_STYLE)

        #Assignee
        assignee = self.__remove_underscores__(self.issue.assignee)
        sheet.write_merge(r1=self.row+12, c1=self.column+0,
                          r2=self.row+12, c2=self.column+1,
                          label="Assignee:", style=ASSIGNEE_LABEL_STYLE)
        sheet.write_merge(r1=self.row+12, c1=self.column+2,
                          r2=self.row+12, c2=self.column+4,
                          label=assignee, style=ASSIGNEE_STYLE)

        #Tester
        tester = self.__remove_underscores__(self.issue.tester)
        sheet.write_merge(r1=self.row+13, c1=self.column+0,
                          r2=self.row+13, c2=self.column+1,
                          label="Tester:", style=TESTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+13, c1=self.column+2,
                          r2=self.row+13, c2=self.column+4,
                          label=tester, style=TESTER_STYLE)

        #Reporter
        reporter = self.__remove_underscores__(self.issue.reporter)
        sheet.write_merge(r1=self.row+14, c1=self.column+0,
                          r2=self.row+14, c2=self.column+1,
                          label="Reporter:", style=REPORTER_LABEL_STYLE)
        sheet.write_merge(r1=self.row+14, c1=self.column+2,
                          r2=self.row+14, c2=self.column+4,
                          label=reporter, style=REPORTER_STYLE)

        #Story points
        points = self.issue.story_points
        sheet.write_merge(r1=self.row+12, c1=self.column+5,
                          r2=self.row+14, c2=self.column+5,
                          label=points, style=STORY_POINTS_STYLE)

        #Epic
        epic = self.issue.epic_name
        sheet.write_merge(r1=self.row+15, c1=self.column+0,
                          r2=self.row+15, c2=self.column+5,
                          label=epic, style=EPIC_STYLE)

        return sheet

    @staticmethod
    def __format_description__(description):
        return (description, description[:127] + ' ...')[len(description) > 128]

    @staticmethod
    def __remove_underscores__(field):
        return (re.sub('_', ' ', str(field)), 'not assigned')[field is None]


class JiraIssue(object):

    def __init__(self, key):
        self.key = key
        self.env = jira_rpc_init(log)
        client = self.env['client']
        auth = self.env['auth']

        raw_data = client.getIssue(auth, key)
        custom_fields = self.__get_custom_fields__(raw_data)

        self.summary = raw_data.summary
        self.description = raw_data.description
        self.assignee = raw_data.assignee
        self.reporter = raw_data.reporter

        self.tester = self.__get_custom_field_value__(custom_fields, TESTER)
        self.story_points = self.__get_custom_field_value__(custom_fields, STORY_POINTS)
        self.team = self.__get_custom_field_value__(custom_fields, TEAM)
        self.desk_check = (False, True)[self.__get_custom_field_value__(custom_fields, DESK_CHECK) == 'Yes']

        estimation_date = self.__get_custom_field_value__(custom_fields, ESTIMATION_DATE)
        if estimation_date:
            try:
                time_struct = strptime(estimation_date, "%d/%b/%y")
                self.estimation_date = datetime.fromtimestamp(mktime(time_struct))
            except TypeError:
                log.warn('Issue {key} does not have valid estimation date'.format(key=key))

        epic = client.getIssue(auth, self.__get_custom_field_value__(custom_fields, EPIC_NAME))
        self.epic_key = epic.key
        self.epic_name = epic.summary

    @staticmethod
    def __get_custom_fields__(raw_data):
        result = dict()
        if raw_data:
            for node in raw_data:
                if type(node) == SOAPpy.Types.typedArrayType:
                    for item in node:
                        try:
                            result[item.customfieldId] = item.values[0]
                        except AttributeError:
                            continue
        return result

    @staticmethod
    def __get_custom_field_value__(custom_fields_dict, name):
        value = None
        if custom_fields_dict:
            value = custom_fields_dict.get(name, None)
        return value