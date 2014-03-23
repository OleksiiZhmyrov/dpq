
from django.core.management.base import BaseCommand, CommandError
from queue.confluence import update_sprint_goals


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Updating stories status on Stories vs Goals KB page')

        try:
            update_sprint_goals()
        except CommandError:
            self.stdout.write('Error while updating stories status on Stories vs Goals KB page')
