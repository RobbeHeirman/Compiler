"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import test.AbstractTests as AbstractTest


class SAssignmentTest(AbstractTest.SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path += "Assignment/"
        self.result_path += "assignment/"

    def test_happy_day(self):
        return self._run_analysis("happy_day.c", 0, 0)
