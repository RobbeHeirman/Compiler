"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import test.AbstractTests as AbstractTest


class LLVMWhileTest(AbstractTest.LLVMAbstractExecTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "while/"
        self.result_path += "while/"

    def test_happy_day(self):
        return self._build_and_run_llvm("happy_day.c", 5)


class MipsConditionalTest(AbstractTest.MipsAbstractTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path += "while/"
        self.result_path += "while/"

    def test_happy_day(self):
        return self._build_and_run_mips("happy_day.c", 5)
