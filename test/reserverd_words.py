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

    def test_happy_const(self):
        return self._run_analysis("happy_const.c", 0)

    def test_wrong_const(self):
        return self._run_analysis("const.c", 1)

    def test_happy_break(self):
        return self._run_analysis("happy_const.c")

    def test_misplaced_break(self):
        return self._run_analysis("misplaced_break.c", 2)
