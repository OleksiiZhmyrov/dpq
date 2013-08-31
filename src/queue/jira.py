import SOAPpy
import re
from dpq.settings import *

soap = SOAPpy.WSDL.Proxy(JIRA_URL)


class JIRAStory:
    def __init__(self, key, summary, description, assignee, tester, reporter, points, epic):
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

    def __init__(self, key):
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


def fetch_story(key):
    return JIRAStory(key)
