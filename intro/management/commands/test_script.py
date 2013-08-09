from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'A test script'

    def handle(self, *args, **options):
            print 'Working test script!'