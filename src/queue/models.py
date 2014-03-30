from django.db import models
from django.contrib.auth.models import User
import re


class Statistics(models.Model):
    date = models.DateField('Date', auto_now_add=True)
    number_of_pushes = models.PositiveIntegerField(default=0)
    total_push_duration = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.date.isoformat() + ": " + \
               str(self.number_of_pushes) + " pushes total, avg. push time is " + \
               str(self.total_push_duration / self.number_of_pushes) + " mins"

    def get_record(self):
        """
        Calculates average push duration in minutes for date.
        Returns tuple [date, average push duration]

        :return:
        """
        return [str(self.date.isoformat()), int(self.total_push_duration / self.number_of_pushes)]


class Branch(models.Model):
    start_date = models.DateField('StartDate', auto_now_add=True)
    finish_date = models.DateField('FinishDate', null=True, blank=True)
    name = models.CharField('Name', max_length=32, unique=True)
    is_active = models.BooleanField()
    build_success = models.BooleanField()
    last_build_date = models.DateTimeField('Last Build date and time', null=True, blank=True)

    def get_status(self):
        """
        Returns branch status: active or inactive.

        :return:
        """
        if self.is_active:
            return 'active'
        else:
            return 'inactive'

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField('Name', max_length=32)
    label = models.CharField('Label', max_length=32)
    css_icon = models.CharField('CSS Icon', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name


class UserStory(models.Model):
    key = models.CharField("Key", max_length=16)
    summary = models.CharField("Summary", max_length=256)
    assignee = models.CharField("Assignee (developer)", max_length=64)
    tester = models.CharField("Tester", max_length=256)
    last_sync = models.DateTimeField('Sync with JIRA on', blank=True, null=True)

    def __unicode__(self):
        return '[{key}] {summary} ({assignee})'.format(key=self.key, summary=self.summary[:32], assignee=self.assignee)

    def is_jira_story(self):
        pattern = PROJECT_NAME + "-?[1-9]{1,3}[0-9]"
        p = re.compile(pattern)
        return p.match(self.key)


class QueueRecord(models.Model):
    story = models.ForeignKey(UserStory)
    owner = models.ForeignKey(User)
    queue_id = models.CharField("ID", max_length=32, unique=True)
    index = models.PositiveIntegerField(unique=True)
    branch = models.ForeignKey(Branch)
    team = models.ForeignKey(Team, blank=True, null=True)
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
    modified_date = models.DateTimeField('Modification Date', auto_now=True)
    push_date = models.DateTimeField('Push Date', blank=True, null=True)
    done_date = models.DateTimeField('Done Date', blank=True, null=True)
    WAITING = "W"
    IN_PROGRESS = "P"
    REVERTED = "R"
    DONE = "D"
    SKIPPED = "S"
    JOKER_MODE = "J"
    STATUS_CHOICES = (
        (WAITING, 'waiting'),
        (IN_PROGRESS, 'in progress'),
        (REVERTED, 'reverted'),
        (DONE, 'done'),
        (SKIPPED, 'skipped'),
        (JOKER_MODE, 'Joker mode'),
    )
    status = models.CharField("status", max_length=1, choices=STATUS_CHOICES, default=WAITING)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return '{index}. {key}: {summary} ({assignee})'.format(index=self.index, key=self.story.key,
                                                               summary=self.story.summary[:32],
                                                               assignee=self.story.assignee)

    def push_duration(self):
        """
        Calculates and returns push duration in minutes.

        :return:
        """
        if self.push_date is not None and self.done_date is not None:
            duration = self.done_date - self.push_date
            return int(duration.total_seconds() / 60.0)
        else:
            return 0


class Role(models.Model):
    description = models.CharField('Description', max_length=64)
    can_create_records = models.BooleanField('Can create records', default=True)
    can_modify_own_records = models.BooleanField('Can modify own records', default=True)
    can_modify_all_records = models.BooleanField('Can modify all records', default=False)

    def __unicode__(self):
        return self.description


class CustomUserRecord(models.Model):
    django_user = models.ForeignKey(User)
    role = models.ForeignKey(Role)
    trump_cards = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return '{username} ({role}, {trump_cards} jokers)'.format(username=self.django_user.username,
                                                                  role=self.role.description,
                                                                  trump_cards=self.trump_cards)


class Sprint(models.Model):
    description = models.CharField('Description', max_length=128, null=True, blank=True)
    number = models.IntegerField('Number')
    motto = models.CharField('Motto', max_length=128, null=True, blank=True)
    start_date = models.DateTimeField('Start Date', blank=True, null=True)
    finish_date = models.DateTimeField('Finish Date', blank=True, null=True)

    def __unicode__(self):
        return 'Sprint {number}'.format(number=self.number)


class RetroBoard(models.Model):
    sprint = models.ForeignKey(Sprint)
    team = models.ForeignKey(Team)
    created_by = models.ForeignKey(CustomUserRecord)
    vote_limit = models.IntegerField('Vote Limit', default=3)
    creation_date = models.DateTimeField('Creation Date', auto_now_add=True)
    is_active = models.BooleanField('Is Active', default=True)

    def __unicode__(self):
        return '{team} board for sprint {sprint}'.format(team=self.team, sprint=self.sprint.number)


class BoardSticker(models.Model):
    created_by = models.ForeignKey(CustomUserRecord)
    retroBoard = models.ForeignKey(RetroBoard)
    creation_date = models.DateTimeField('Creation Date', auto_now_add=True)
    modification_date = models.DateTimeField('Modification Date', blank=True, null=True)
    is_modified = models.BooleanField('Is Modified', default=False)
    summary = models.CharField('Description', max_length=512, null=True, blank=True)
    votes = models.IntegerField(default=0)
    voters = models.CharField('Voters', max_length=512, null=True, blank=True)
    is_completed = models.BooleanField('Is Completed', default=False)
    status_code = models.PositiveSmallIntegerField('Status code', default=0, null=True, blank=True)
    GOOD = "G"
    CHANGE = "C"
    ACTION = "A"
    TYPE_CHOICES = (
        (GOOD, 'was good'),
        (CHANGE, 'need to change'),
        (ACTION, 'action point'),
    )
    type = models.CharField("type", max_length=1, choices=TYPE_CHOICES, default=CHANGE)

    def __unicode__(self):
        return 'Sticker ({type}, {votes} votes, sprint {sprint}: {summary} )'.format(type=self.type, votes=self.votes,
                                                                                     sprint=self.retroBoard.sprint,
                                                                                     summary=self.summary)

class UserToRetroBoardConnector(models.Model):
    custom_user_record = models.ForeignKey(CustomUserRecord)
    retroBoard = models.ForeignKey(RetroBoard)
    votes = models.IntegerField(default=0)


class ConfluenceSettings(models.Model):
    # This model is experimental
    # TODO: Must be replaced with proper code later
    login = models.CharField('Login', max_length=20, null=True, blank=True)
    password = models.CharField('Password', max_length=64, null=True, blank=True)
    url = models.CharField('URL', max_length=128, null=True, blank=True)
    namespace = models.CharField('Namespace', max_length=32, null=True, blank=True)
    SvG_page_title = models.CharField('Stories vs Goals Page title', max_length=64, null=True, blank=True)

    def __unicode__(self):
        return '{namespace}: {page_title}'.format(namespace=self.namespace, page_title=self.SvG_page_title)


class JiraSettings(models.Model):
    # This model is experimental
    # TODO: Must be replaced with proper code later
    login = models.CharField('Login', max_length=20, null=True, blank=True)
    password = models.CharField('Password', max_length=64, null=True, blank=True)
    url = models.CharField('WADL URL', max_length=128, null=True, blank=True)
    browse_url = models.CharField('Browse URL', max_length=128, null=True, blank=True)
    project_name = models.CharField('Project Name', max_length=64, null=True, blank=True)

    custom_field_story_points = models.CharField('Custom field: story points', null=True, max_length=32, default='')
    custom_field_epic_name = models.CharField('Custom field: epic name', null=True, max_length=32, default='')
    custom_field_tester = models.CharField('Custom field: tester', null=True, max_length=32, default='')
    custom_field_team = models.CharField('Custom field: team', null=True, max_length=32, default='')
    custom_field_estimation_date = models.CharField('Custom field: est. date', null=True, max_length=32, default='')
    custom_field_desk_check = models.CharField('Custom field: is desk check', null=True, max_length=32, default='')
    custom_field_onshore_ba = models.CharField('Custom field: onshore BA', null=True, max_length=32, default='')

    def __unicode__(self):
        return 'Jira settings: {login}'.format(login=self.login)


class DeskCheckStatistic(models.Model):
    creation_date = models.DateTimeField('Creation Date', auto_now_add=True)
    total_count = models.FloatField('Total story count')
    total_count_sp = models.FloatField('Total story points count')
    other_count = models.FloatField('Stories ToDo count')
    other_count_sp = models.FloatField('Story points ToDo count')
    other_percent = models.FloatField('Stories ToDo percent')
    other_percent_sp = models.FloatField('Story points ToDo percents')
    passed_count = models.FloatField('Stories Passed count')
    passed_count_sp = models.FloatField('Story points Passed count')
    passed_percent = models.FloatField('Stories Passed percent')
    passed_percent_sp = models.FloatField('Story points Passed percents')
    ready_count = models.FloatField('Stories Ready count')
    ready_count_sp = models.FloatField('Story points Ready count')
    ready_percent = models.FloatField('Stories Ready percent')
    ready_percent_sp = models.FloatField('Story points Ready percents')
    failed_count = models.FloatField('Stories Failed count')
    failed_count_sp = models.FloatField('Story points Failed count')
    failed_percent = models.FloatField('Stories Failed percent')
    failed_percent_sp = models.FloatField('Story points Failed percents')

    def __unicode__(self):
        return 'Desk check stats for {date}'.format(date=self.creation_date)


class OutdatedJiraIssue(models.Model):
    key = models.CharField('Key', max_length=32)
    summary = models.CharField('Summary', max_length=1024, null=True, blank=True)
    description = models.CharField('Description', max_length=1024, null=True, blank=True)
    assignee = models.CharField('Assignee', max_length=64, null=True, blank=True)
    tester = models.CharField('Tester', max_length=64, null=True, blank=True)
    reporter = models.CharField('Reporter', max_length=64, null=True, blank=True)
    points = models.IntegerField('Story Points', default=0)
    epic = models.CharField('Epic', max_length=32, null=True, blank=True)
    team = models.CharField('Team', max_length=32, null=True, blank=True)
    is_deskcheck = models.BooleanField('Is Desk check story', default=False)
    estimation_date = models.DateField('Estimation date', null=True, blank=True)
