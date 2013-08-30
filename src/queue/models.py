from django.db import models
from django.contrib.auth.models import User


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
    key = models.CharField("Key", max_length=16, unique=True)
    summary = models.CharField("Summary", max_length=256)
    assignee = models.CharField("Assignee (developer)", max_length=64)
    tester = models.CharField("Tester", max_length=256)
    last_sync = models.DateTimeField('Sync with JIRA on', blank=True, null=True)

    def __unicode__(self):
        return '[{key}] {summary} ({assignee})'.format(key=self.key, summary=self.summary[:32], assignee=self.assignee)


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
    STATUS_CHOICES = (
        (WAITING, 'waiting'),
        (IN_PROGRESS, 'in progress'),
        (REVERTED, 'reverted'),
        (DONE, 'done'),
        (SKIPPED, 'skipped'),
    )
    status = models.CharField("status", max_length=1, choices=STATUS_CHOICES, default=WAITING)

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

    def get_record(self):
        return [str(self.ps), int(self.push_duration())]


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

    def __unicode__(self):
        return '{username} ({role})'.format(username=self.django_user.username, role=self.role.description)