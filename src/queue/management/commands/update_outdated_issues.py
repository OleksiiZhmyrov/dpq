
from django.core.management.base import BaseCommand, CommandError
from queue.dpq_util import JiraUtil


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Updating outdated issues')

        try:
            JiraUtil.store_outdated_issues()
        except CommandError:
            self.stdout.write('Error while updating outdated issues')
