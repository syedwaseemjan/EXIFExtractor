# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~
    tests package
"""

import sys
import os
import config as test_config
from unittest import TestCase
from app import config

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


for attribute in dir(config):
    if not attribute.startswith("__"):
        setattr(config, attribute, getattr(test_config, attribute))


class ExifExtractorAppTestCase(TestCase):
    """ ExifExtractorAppTestCase is not doing anything special
    but we can place any common functionality in it in future
    if we want to add more tests.
    """

    def setUp(self):
        super(ExifExtractorAppTestCase, self).setUp()

    def tearDown(self):
        super(ExifExtractorAppTestCase, self).tearDown()
