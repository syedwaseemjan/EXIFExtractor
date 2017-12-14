# -*- coding: utf-8 -*-

from . import ExifExtractorAppTestCase
from app.main import Main


class ServerTestCase(ExifExtractorAppTestCase):
    """
    ServerTestCase constains all unit tests for StatsCollector App.
    """

    def setUp(self):
        super(ServerTestCase, self).setUp()
        Main()
