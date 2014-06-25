# -*- coding: utf-8 -*-

import re

alphabet_regexp = re.compile("[a-z]", re.IGNORECASE)
word_regexp     = re.compile("^[a-z]+$", re.IGNORECASE)
upper_regexp    = re.compile("[A-Z]")
