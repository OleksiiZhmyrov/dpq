import SOAPpy
from bs4 import BeautifulSoup
from queue.dpq_util import JiraUtil, ConfluenceDeskCheckUtil
from queue.models import ConfluenceSettings, DeskCheckStatistic
from time import gmtime, strftime

from logger import LOGGER

confluence_settings = ConfluenceSettings.objects.all()[0]
soap = SOAPpy.WSDL.Proxy(confluence_settings.url)


def __get_page_from_confluence(page_title):
    auth = soap.login(confluence_settings.login, confluence_settings.password)
    page = soap.getPage(auth, confluence_settings.namespace, page_title)
    return page


def update_sprint_goals():
    page_name = confluence_settings.SvG_page_title
    page = __get_page_from_confluence(page_name)
    soup = BeautifulSoup(page.content)

    keys = []
    for item in soup.findAll("tr")[1:]:
        keys.append(item.findAll("td")[-9:][0].find("a").text)

    LOGGER.info(keys)

    stories = {}
    for story in JiraUtil.get_issues(keys):
        stories[story.key] = story

    for item in soup.findAll("tr")[1:]:
        key = item.findAll("td")[-9:][0].find("a").text
        story = stories[key]

        line = item.findAll("td")[-9:]

        status = BeautifulSoup('<td>{status}</td>'.format(status=story.status))
        line[-8].replace_with(status)

        desk_check = BeautifulSoup('<td>{desk_check}</td>'.format(desk_check=story.desk_check))
        line[-7].replace_with(desk_check)

        reporter = BeautifulSoup('<td>{reporter}</td>'.format(reporter=story.reporter))
        line[-5].replace_with(reporter)

        onshore_ba = BeautifulSoup('<td>{onshore_ba}</td>'.format(onshore_ba=story.onshore_ba))
        line[-4].replace_with(onshore_ba)

        story.desk_check_status = unicode(line[-6].text).replace(u'\xa0', '')
        stories[key] = story

    ConfluenceDeskCheckUtil.save_table_records_to_database(stories.values())

    update_message = "Page automatically updated by {login} on {datetime}<br\>"\
        .format(login=confluence_settings.login, datetime=strftime("%Y-%m-%d %H:%M:%S %z", gmtime()))

    npage = {}
    npage["content"] = update_message + unicode(soup.find("table"))
    npage["space"] = page["space"]
    npage["title"] = page["title"]
    npage["id"] = SOAPpy.Types.longType(long(page["id"]))
    npage["version"] = SOAPpy.Types.intType(int(page["version"]))
    npage["parentId"] = SOAPpy.Types.longType(long(page["parentId"]))

    LOGGER.info(npage)

    auth = soap.login(confluence_settings.login, confluence_settings.password)
    soap.storePage(auth, npage)
