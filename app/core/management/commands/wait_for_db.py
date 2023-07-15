"""
Django command to wait for the database to be availabel
"""
from typing import Any, Optional # noqa
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command for wait for db"""

    def handle(self, *args: Any, **options: Any):
        """Entrypoint for command."""

        self.stdout.write("Waiting for db...")

        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, Waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
