
from django.core.management.base import BaseCommand, CommandError
from queue.dpq_util import ConfluenceDeskCheckUtil


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Updating deskcheck issues')

        try:
            ConfluenceDeskCheckUtil.save_statistics()
        except CommandError:
            self.stdout.write('Error while updating deskcheck issues')
