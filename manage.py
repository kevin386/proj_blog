#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if sys.argv[1] == '--pro':
        sys.argv.pop(1)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj_blog.settings_pro")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj_blog.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
