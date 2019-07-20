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

    def test_happy_day_regres(self):
        return self._run_analysis("happy_day_regres.c")

    def test_redeclaration_func(self):
        return self._run_analysis("redeclaration_func.c", errors=1)

    def test_redefinition(self):
        return self._run_analysis("redefinition.c", 1, 0)

    def test_return_conflict(self):
        return self._run_analysis("return_conflict.c", 1)

    def test_signature_call(self):
        return self._run_analysis("signature_call_conflict.c", 2)
