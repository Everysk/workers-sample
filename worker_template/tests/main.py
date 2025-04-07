###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

from unittest import TestCase
from ..main import main

class WorkerSampleTestCase(TestCase):

    def test_main(self):
        args = {
            "input": "input"
        }

        self.assertEqual(main(args), args)
