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


def fetch_story(key):
    auth = soap.login(JIRA_LOGIN, JIRA_PASSWORD)

    try:
        issue = soap.getIssue(auth, key)
    except:
        return None

    story_points = "n/a"
    epic_key = None
    tester = ""

    node = issue[5]
    for i in range(1, len(node) + 1):
        try:
            if node[i].customfieldId in STORY_POINTS_CUSTOM_FIELDS:
                story_points = node[i].values[0]
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

    if epic_key is not None:
        epic = soap.getIssue(auth, epic_key)
        epic_summary = epic.summary
    else:
        epic_summary = "n/a"

    description = issue.description
    description = (description, description[:127] + ' ...')[len(description) > 128]

    assignee = (re.sub('_', ' ', str(issue.assignee)), '')[issue.assignee is None]
    reporter = (re.sub('_', ' ', str(issue.reporter)), '')[issue.reporter is None]
    tester = re.sub('_', ' ', str(tester))

    return JIRAStory(
        key=issue.key,
        summary=issue.summary,
        description=description,
        assignee=assignee,
        tester=tester,
        reporter=reporter,
        points=story_points,
        epic=epic_summary
    )
