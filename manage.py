'''
# Solution for Software Delevopment Test.
#
# Created by MSc. Carlos Andres Sierra on February 2018.
# Copyright (c) 2018  Msc. Carlos Andres Sierra.  All rights reserved.
#
# This file is part of NegotiatusDashboardProject.
#
# NegotiatusDashboardProject is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3.
'''

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. "
        ) 																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																											from exc
    execute_from_command_line(sys.argv)
