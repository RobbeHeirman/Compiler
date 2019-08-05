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

    def test_assign_to_rval(self):
        return self._run_analysis("assign_to_rval.c", 3)

    def test_conversion(self):
        return self._run_analysis("conversions.c", 3)


class LLVMAssignmentTest(AbstractTest.LLVMAbstractExecTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Assignment/"
        self.result_path += "assignment/"

    def test_happy_day(self):
        return self._build_and_run_llvm("happy_day.c", 1)


class MipsFunctionTest(AbstractTest.MipsAbstractTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "Assignment/"
        self.result_path += "assignment/"

    def test_happy_day(self):
        return self._build_and_run_mips("happy_day.c", 1)
