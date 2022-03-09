#!/usr/bin/env python
import os
import sys

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv('.env')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartmove.settings.base")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
