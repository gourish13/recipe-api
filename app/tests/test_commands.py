"""
Test for custom django commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('recipe.management.commands.db_wait.Command.check')
class CommandTest(SimpleTestCase):
    """Test Commands"""

    def test_wait_db_ready(self, patched_check):
        """Test waiting for db connection to be ready"""
        patched_check.return_value = True

        call_command('db_wait')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('db_wait')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
