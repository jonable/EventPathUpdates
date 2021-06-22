#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventupdates.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
