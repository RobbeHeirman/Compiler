"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import test.AbstractTests as AbstractTest


class SreservedTest(AbstractTest.SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "reserved_words/"
        self.result_path += "reserved_words/"

    def test_happy_day(self):
        return self._run_analysis("const.c", 1)
