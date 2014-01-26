import logging
import sys
import SOAPpy
from queue.models import JiraSettings, ConfluenceSettings


jira_settings = JiraSettings.objects.all()[0]
confluence_settings = ConfluenceSettings.objects.all()[0]

JIRA_WSDL_URL = jira_settings.url
JIRA_USERNAME = jira_settings.login
JIRA_PASSWORD = jira_settings.password
JIRA_PROJECT_NAME = jira_settings.project_name

CONFLUENCE_WSDL_URL = confluence_settings.url
CONFLUENCE_USERNAME = confluence_settings.login
CONFLUENCE_PASSWORD = confluence_settings.password
CONFLUENCE_NAMESPACE = confluence_settings.namespace
CONFLUENCE_PAGE_TITLE = confluence_settings.page_title


def setup_logging(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_jira_client(logger):
    try:
        logger.debug('Attempting to connect to the server: ' + JIRA_WSDL_URL)
        soap = SOAPpy.WSDL.Proxy(JIRA_WSDL_URL)
        logger.debug('Connected to the server')

        return soap
    except Exception, e:
        logger.error('Failed to connect to JIRA (%s): %s' % (JIRA_WSDL_URL, e))
        raise


def jira_rpc_init(logger):
    env = dict(
        jira_username=JIRA_USERNAME,
        jira_password=JIRA_PASSWORD
    )

    try:
        logger.debug('Starting authorization')

        client = get_jira_client(logger)
        auth = client.login(
            JIRA_USERNAME, JIRA_PASSWORD
        )

        env['user'] = client.getUser(auth)
        env['client'] = client
        env['auth'] = auth
        env['project_name'] = JIRA_PROJECT_NAME
    except Exception, e:
        logger.error('Error authenticating with JIRA')
        logger.exception(e)
        raise

    return env


def get_confluence_client(logger):
    try:
        logger.debug('Attempting to connect to the server: ' + CONFLUENCE_WSDL_URL)
        soap = SOAPpy.WSDL.Proxy(CONFLUENCE_WSDL_URL)
        logger.debug('Connected to the server')

        return soap
    except Exception, e:
        logger.error('Failed to connect to Confluence (%s): %s' % (CONFLUENCE_WSDL_URL, e))
        raise


def confluence_rpc_init(logger):
    env = dict(
        confluence_username=CONFLUENCE_USERNAME,
        confluence_password=CONFLUENCE_PASSWORD
    )

    try:
        logger.debug('Starting authorization')

        client = get_confluence_client(logger)
        auth = client.login(CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)

        env['client'] = client
        env['auth'] = auth
        env['namespace'] = CONFLUENCE_NAMESPACE
        env['page_title'] = CONFLUENCE_PAGE_TITLE
    except Exception, e:
        logger.error('Error authenticating on Confluence with login {login}'.format(login=CONFLUENCE_USERNAME))
        logger.exception(e)
        raise

    return env