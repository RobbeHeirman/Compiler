"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import test.AbstractTests as AbstractTest


class ArithmeticTest(AbstractTest.SAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path += "Arithmetic/"
        self.result_path += "arithmetic/"

    def test_happy_day(self):
        return self._run_analysis("happy_day.c")

    def test_happy_day2(self):
        return self._run_analysis("happy_day2.c")

    def test_wrong_types(self):
        return self._run_analysis("wrong_types.c", 1)


class LLVMArithmeticTest(AbstractTest.LLVMAbstractExecTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path += "Arithmetic/"
        self.result_path += "arithmetic/"

    def test_happy_day(self):
        return self._build_and_run_llvm("happy_day.c", 532)

    def test_happy_day2(self):
        return self._build_and_run_llvm("happy_day2.c", 3)


class MipsArithmeticTest(AbstractTest.MipsAbstractTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
