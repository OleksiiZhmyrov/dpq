from django.db import models
from django.contrib.auth.models import User


class Statistics(models.Model):
    date = models.DateField('Date', auto_now_add = True)
    number_of_pushes = models.PositiveIntegerField(default = 0)
    total_push_duration = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return self.date.isoformat() + ": " + \
            str(self.number_of_pushes) + " pushes total, avg. push time is " + \
            str(self.total_push_duration / self.number_of_pushes) + " mins"

    def get_record(self):
        return [str(self.date.isoformat()), int(self.total_push_duration / self.number_of_pushes)]


class Branch(models.Model):
	start_date = models.DateField('StartDate', auto_now_add = True)
	finish_date = models.DateField('FinishDate', null = True, blank = True)
	name = models.CharField('Name', max_length = 32, unique = True)
	is_active = models.BooleanField()
	
	def get_status(self):
		if self.is_active == True:
			return 'active'
		else:
			return 'inactive'
	
	def __unicode__(self):
		return self.name


class Queue(models.Model):
    ps = models.CharField("ps", max_length = 10)
    owner = models.ForeignKey(User)
    developerA = models.CharField("developerA", max_length = 64)
    developerB = models.CharField("developerB", max_length = 64, null = True)
    tester = models.CharField("tester", max_length = 64)
    queue_id = models.CharField("id", max_length = 32, unique = True)
    index = models.PositiveIntegerField(unique = True)
    description = models.CharField("description", max_length = 128)
    branch = models.ForeignKey(Branch)
    creation_date = models.DateTimeField('Creation date', auto_now_add = True)
    modified_date = models.DateTimeField('Modification Date', auto_now = True)
    push_date = models.DateTimeField('Push Date', blank = True, null = True)
    done_date = models.DateTimeField('Done Date', blank = True, null = True)
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
    status = models.CharField("status", max_length = 1, choices = STATUS_CHOICES, default = WAITING)

    def __unicode__(self):
        return self.ps + ": " + self.description

    def push_duration(self):
        if(self.push_date != None and self.done_date != None):
            duration = self.done_date - self.push_date
            return int(duration.total_seconds()/60.0)
        else:
            return 0

    def get_record(self):
        return [str(self.ps), int(self.push_duration())]
