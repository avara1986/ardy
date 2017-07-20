#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import arrow

def my_handler(event, context):

    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    date_to_print = local.humanize()

    message = 'Hello world lambda1! at {}'.format(date_to_print)
    return {
        'message': message
    }
