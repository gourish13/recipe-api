"""
Custom django command to wait for database to be ready for connection
"""

import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db connection"""

    def handle(self, *args, **options):
        """Command Entrypoint"""
        self.stdout.write('Waiting for database connection...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database not ready for connection, \
                                  retrying in 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Connection available'))
