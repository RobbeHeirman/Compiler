"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from test.AbstractTests import SAbstractTest


class FunctionTest(SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Function/"
        self.result_path += "function/"

    def test_main_happy_day(self):
        self._run_analysis("main_happy_day.c")
